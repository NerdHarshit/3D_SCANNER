import numpy as np
import open3d as o3d
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

        return self.layerCount , x ,y ,z


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
