# gui.py
import tkinter as tk
from tkinter import ttk, messagebox

class ScannerGUI:
    def __init__(self, root, on_start, on_stop, on_save_checkpoint, batch_default=50):
        self.root = root
        self.on_start = on_start
        self.on_stop = on_stop
        self.on_save_checkpoint = on_save_checkpoint

        self.status_var = tk.StringVar(value="Idle")
        self.last_msg_var = tk.StringVar(value="")
        self.sent_flag_var = tk.StringVar(value="")
        self.points_var = tk.IntVar(value=0)
        self.layers_var = tk.IntVar(value=0)
        self.batch_var = tk.IntVar(value=batch_default)

        self._build_ui()

    def _build_ui(self):
        frm = ttk.Frame(self.root, padding=10)
        frm.grid(row=0, column=0, sticky="nsew")

        btn_frame = ttk.Frame(frm)
        btn_frame.grid(row=0, column=0, sticky="w")
        self.start_btn = ttk.Button(btn_frame, text="Start", command=self.on_start)
        self.start_btn.grid(row=0, column=0, padx=4)
        self.stop_btn = ttk.Button(btn_frame, text="Stop", command=self.on_stop, state="disabled")
        self.stop_btn.grid(row=0, column=1, padx=4)
        self.save_btn = ttk.Button(btn_frame, text="Save Checkpoint", command=self.on_save_checkpoint)
        self.save_btn.grid(row=0, column=2, padx=4)

        ttk.Label(frm, text="Status:").grid(row=1, column=0, sticky="w")
        ttk.Label(frm, textvariable=self.status_var).grid(row=1, column=1, sticky="w")

        ttk.Label(frm, text="Last Msg:").grid(row=2, column=0, sticky="w")
        ttk.Label(frm, textvariable=self.last_msg_var, width=40).grid(row=2, column=1, sticky="w")

        ttk.Label(frm, text="Sent Flag:").grid(row=3, column=0, sticky="w")
        ttk.Label(frm, textvariable=self.sent_flag_var).grid(row=3, column=1, sticky="w")

        ttk.Label(frm, text="Points:").grid(row=4, column=0, sticky="w")
        ttk.Label(frm, textvariable=self.points_var).grid(row=4, column=1, sticky="w")

        ttk.Label(frm, text="Layers:").grid(row=5, column=0, sticky="w")
        ttk.Label(frm, textvariable=self.layers_var).grid(row=5, column=1, sticky="w")

        ttk.Label(frm, text="Plot batch size (points):").grid(row=6, column=0, sticky="w")
        ttk.Entry(frm, textvariable=self.batch_var, width=8).grid(row=6, column=1, sticky="w")

    # helpers to enable/disable buttons from main
    def set_running(self, running: bool):
        self.start_btn.config(state="disabled" if running else "normal")
        self.stop_btn.config(state="normal" if running else "disabled")

    # update methods called from main thread
    def update_status(self, status):
        self.status_var.set(status)

    def update_last_msg(self, msg):
        self.last_msg_var.set(msg)

    def update_sent_flag(self, flag):
        self.sent_flag_var.set(flag)

    def update_points(self, count):
        self.points_var.set(count)

    def update_layers(self, count):
        self.layers_var.set(count)

    def get_batch_size(self):
        try:
            return int(self.batch_var.get())
        except Exception:
            return 50
