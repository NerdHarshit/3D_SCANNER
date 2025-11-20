import numpy as np

class PlotManager:

    def __init__(self):
        self.h_list = []
        self.d_list = []
        self.theta_list = []
        self.layerCount = 0

    def append_point_cyl(self,h,d,theta_deg):
        self.h_list.append(float(h))
        self.d_list.append(float(d))
        self.theta_list.append(float(theta_deg))

    def getXYZ(self):
        if len(self.h_list) ==0:
            return(np.empty((0,3),dtype=float))
        
        h = np.array(self.h_list,dtype=float)
        d = np.array(self.d_list,dtype=float)
        theta = np.array(self.theta_list,dtype=float)
        theta_rad = np.deg2rad(theta)

        x = d*np.cos(theta_rad)
        y = d*np.sin(theta_rad)
        z = h
        pts = np.vstack((x,y,z)).T
        return pts
    
    def resetLayer(self):
        self.layerCount +=1
        #right now just increments layer count
        #can be extended to do more complex tasks if needed

    def get_counts(self):
        return len(self.h_list), self.layerCount