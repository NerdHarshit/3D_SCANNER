# live_plot.py
import time
import numpy as np

def plotter_process(point_queue, control_queue):
    """
    Plotter process target. Expects:
      - point_queue: multiprocessing.Queue of numpy arrays (Nx3) to append/display
      - control_queue: for 'clear' and 'exit'
    """
    try:
        import open3d as o3d
    except Exception as e:
        print("[live_plot] Open3D not available:", e)
        return

    vis = o3d.visualization.Visualizer()
    vis.create_window(window_name="3D Scanner Live View", width=960, height=720)
    pcd = o3d.geometry.PointCloud()
    vis.add_geometry(pcd)
    points_np = np.empty((0,3), dtype=float)
    opt = vis.get_render_option()
    opt.point_size = 2.0

    try:
        while True:
            # handle control
            try:
                cmd = control_queue.get_nowait()
            except Exception:
                cmd = None
            if cmd == "exit":
                break
            if cmd == "clear":
                points_np = np.empty((0,3), dtype=float)
                pcd.points = o3d.utility.Vector3dVector(points_np)
                vis.update_geometry(pcd)

            # drain incoming point batches
            got = False
            while True:
                try:
                    arr = point_queue.get_nowait()
                    if isinstance(arr, np.ndarray) and arr.size:
                        points_np = np.vstack((points_np, arr))
                        got = True
                except Exception:
                    break

            if got:
                pcd.points = o3d.utility.Vector3dVector(points_np)
                vis.update_geometry(pcd)

            vis.poll_events()
            vis.update_renderer()
            time.sleep(0.01)

    except KeyboardInterrupt:
        pass
    finally:
        vis.destroy_window()
