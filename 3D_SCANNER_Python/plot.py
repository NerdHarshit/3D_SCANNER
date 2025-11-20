import numpy as np
import time

def plotter_process(point_queue,control_queue):

    try:
        import open3d as o3d

    except ImportError as e:
        print("open3d not available:",e)
        return
    
    vis = o3d.visualization.Visualizer()
    vis.create_window(window_name = "3D scanner live viee",width=960,height = 720)

    pcd = o3d.geometry.PointCloud()
    vis.add_geometry(pcd)

    points_np = np.empty((0,3),dtype=float)
    opt = vis.get_render_option()
    opt.point_size =2.0
    opt.background_color = [0,0,0]

    try:
        while True:
            try:
                cmd = control_queue.get_nowait()

            except Exception:
                cmd = None
            
            if cmd == "exit":
                break

            if cmd == "clear":
                points_np = np.empty((0,3),dtype=float)
                pcd.points = o3d.utility.Vector3dVector(points_np)
                vis.update_geometry(pcd)

            got = False
            while True:
                try:
                    arr = point_queue.get_nowait()
                    if isinstance(arr,np.ndarray) and arr.size:
                        points_np = np.vstack((points_np,arr))
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



'''
older method
class MY_3D:

    def __init__(self,H,D,Theta):
        self.h_list = H
        self.d_list = D
        self.theta_list = Theta
        self.layerCount = 0

    def convertToXYZ(self):
        #onverts cylindrical to XYZ coordinates

        if len(self.h_list) ==0:
            return np.array([]),np.array([]),np.array([])
        
        h = np.array(self.h_list,dtype=float)
        d = np.array(self.d_list,dtype=float)
        theta = np.array(self.theta_list,dtype=float)

        theta_rad = np.deg2rad(theta)

        x = d * np.cos(theta_rad)
        y = d * np.sin(theta_rad)
        z = h

        return x ,y,z

    
    def plotLayer(self):
        x ,y ,z = self.convertToXYZ()

        if(len(x) ==0):
            print("No data to plot")
            return self.layerCount , x ,y ,z #list or array here? for xyz
        
        points = np.vstack((x,y,z)).T

        pcd = o3d.geometry.PointCloud()
        pcd.points = o3d.utility.Vector3dVector(points)

        print("Plotting layer number;",self.layerCount +1, "with",len(points),"points")

        o3d.visualization.draw_geometries([pcd])

        self.layerCount +=1

        return self.layerCount , x ,y ,z'''


'''pcd = o3d.io.read_point_cloud("3D_SCANNER_Python\pretty_point_cloud.ply")

vis = o3d.visualization.Visualizer()
vis.create_window(window_name="Pretty Cloud - Enhanced", width=1280, height=720)
vis.add_geometry(pcd)

opt = vis.get_render_option()
opt.background_color = [0.05, 0.05, 0.05]   # dark background
opt.point_size = 3.0                        # larger points
opt.show_coordinate_frame = True

vis.run()
vis.destroy_window()'''
