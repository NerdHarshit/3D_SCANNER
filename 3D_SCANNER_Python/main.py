# main.py
import multiprocessing as mp
import threading
import time
import numpy as np
import csv
from pathlib import Path

from serialIO import MY_Serial
from plotManager import PlotManager
from plot import plotter_process
from gui import ScannerGUI

# Config
COM_PORT = "COM5"
BAUDRATE = 9600
CSV_CHECKPOINT = "scan_checkpoint.csv"
RECONNECT_DELAY = 3
CSV_EVERY_POINTS = 200

def write_checkpoint_csv(h_list, d_list, theta_list, filename):
    p = Path(filename)
    write_header = not p.exists()
    with p.open("a", newline="") as f:
        writer = csv.writer(f)
        if write_header:
            writer.writerow(["h","d","theta"])
        for i in range(len(h_list)):
            writer.writerow([h_list[i], d_list[i], theta_list[i]])

def serial_thread_fn(serial_factory, plot_manager: PlotManager, point_queue: mp.Queue, gui_state: dict, stop_event: threading.Event):
    """
    Reads serial, appends to plot_manager, and sends batched xyz arrays to point_queue.
    gui_state is a dict shared with main for status display (not thread-synchronized locks for simplicity).
    """
    # create serial instance (factory should construct MY_Serial)
    ser = None
    while not stop_event.is_set():
        try:
            ser = serial_factory()
            gui_state['status'] = f"Connected: {ser.port}"
            break
        except Exception as e:
            gui_state['status'] = f"Serial open failed: {e}. Retrying..."
            time.sleep(RECONNECT_DELAY)

    if stop_event.is_set():
        return

    # wait for START?
    gui_state['status'] = "Waiting for START?"
    while not stop_event.is_set():
        line = ser.readline()
        gui_state['last_msg'] = line
        if line == "START?":
            ser.pyStartScan()
            gui_state['sent_flag'] = "PY_READY"
            gui_state['status'] = "Scanning"
            break

    batch = []
    total_points = 0
    checkpoint_counter = 0
    try:
        while not stop_event.is_set():
            line = ser.readline()
            if not line:
                continue
            gui_state['last_msg'] = line

            if line == "LAYER_OVER":
                gui_state['layers'] += 1
                # flush batch
                if batch:
                    arr = np.vstack(batch)
                    try:
                        point_queue.put_nowait(arr)
                    except Exception:
                        pass
                    batch = []
                # checkpoint current data
                write_checkpoint_csv(plot_manager.h_list, plot_manager.d_list, plot_manager.theta_list, CSV_CHECKPOINT)
                ser.startNextLayer()
                gui_state['sent_flag'] = "PY_READY_FOR_NEXT_LAYER"
                continue

            if line == "SCAN_OVER":
                # final checkpoint
                write_checkpoint_csv(plot_manager.h_list, plot_manager.d_list, plot_manager.theta_list, CSV_CHECKPOINT)
                ser.scanOverAck()
                gui_state['sent_flag'] = "SCAN_OVER_ACK"
                gui_state['status'] = "Scan finished"
                break

            if line.startswith("datapoint="):
                try:
                    data = line.split("=",1)[1]
                    h,d,theta = data.split("/")
                    h_f = float(h); d_f = float(d); th_f = float(theta)
                except Exception as e:
                    gui_state['status'] = f"Parse error: {e}"
                    continue

                # store canonical data
                plot_manager.append_point_cyl(h_f, d_f, th_f)
                total_points += 1
                checkpoint_counter += 1
                gui_state['points'] = total_points

                # create xyz and append to local batch
                th_rad = np.deg2rad(th_f)
                x = d_f * np.cos(th_rad)
                y = d_f * np.sin(th_rad)
                z = h_f
                batch.append(np.array([x,y,z], dtype=float))

                # if enough points, push to plot process
                batch_size = gui_state.get('batch_size', 50)
                if len(batch) >= batch_size:
                    arr = np.vstack(batch)
                    try:
                        point_queue.put_nowait(arr)
                    except Exception:
                        pass
                    batch = []

                # periodic checkpoint
                if checkpoint_counter >= CSV_EVERY_POINTS:
                    write_checkpoint_csv(plot_manager.h_list, plot_manager.d_list, plot_manager.theta_list, CSV_CHECKPOINT)
                    checkpoint_counter = 0

            # else ignore unknown lines

    except Exception as e:
        gui_state['status'] = f"Serial thread error: {e}"
    finally:
        gui_state['status'] = "Serial thread stopped"

def main():
    mp.set_start_method('spawn')  # safe across platforms

    # shared app state for GUI (simple dict)
    gui_state = {
        'status': 'Idle',
        'last_msg': '',
        'sent_flag': '',
        'points': 0,
        'layers': 0,
        'batch_size': 50
    }

    plot_manager = PlotManager()

    # create queues and plotter process
    point_queue = mp.Queue(maxsize=10000)
    control_queue = mp.Queue()
    plot_proc = mp.Process(target=plotter_process, args=(point_queue, control_queue), daemon=True)
    plot_proc.start()

    # set up GUI
    import tkinter as tk
    root = tk.Tk()

    # callback functions
    stop_event = threading.Event()
    serial_thread = None

    def start_cb():
        nonlocal serial_thread, stop_event
        stop_event.clear()
        gui_state['status'] = "Starting..."
        gui_widget.set_running(True)
        gui_widget.update_status("Starting...")
        # start serial thread
        serial_thread = threading.Thread(target=serial_thread_fn,
                                         args=(lambda: MY_Serial(port=COM_PORT, baudrate=BAUDRATE, timeout=2),
                                               plot_manager, point_queue, gui_state, stop_event),
                                         daemon=True)
        serial_thread.start()

    def stop_cb():
        nonlocal serial_thread, stop_event
        stop_event.set()
        if serial_thread:
            serial_thread.join(timeout=2)
        # stop plot process
        try:
            control_queue.put_nowait("exit")
            plot_proc.join(timeout=2)
        except Exception:
            pass
        gui_widget.set_running(False)
        gui_widget.update_status("Stopped")

    def save_checkpoint_cb():
        write_checkpoint_csv(plot_manager.h_list, plot_manager.d_list, plot_manager.theta_list, CSV_CHECKPOINT)

    gui_widget = ScannerGUI(root, on_start=start_cb, on_stop=stop_cb, on_save_checkpoint=save_checkpoint_cb, batch_default=50)

    # periodic GUI refresh (reads gui_state)
    def refresh():
        gui_widget.update_status(gui_state.get('status',''))
        gui_widget.update_last_msg(gui_state.get('last_msg',''))
        gui_widget.update_sent_flag(gui_state.get('sent_flag',''))
        gui_widget.update_points(gui_state.get('points',0))
        gui_widget.update_layers(gui_state.get('layers',0))
        # propagate batch size to gui_state
        gui_state['batch_size'] = gui_widget.get_batch_size()
        root.after(200, refresh)

    root.after(200, refresh)

    try:
        root.mainloop()
    finally:
        # cleanup on exit
        stop_event.set()
        try:
            control_queue.put_nowait("exit")
        except Exception:
            pass
        try:
            plot_proc.terminate()
        except Exception:
            pass

if __name__ == "__main__":
    main()
