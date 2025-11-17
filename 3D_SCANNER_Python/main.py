#this will contain the gui for getting point cloud from csv and also for visualizing the point cloud
from serialIO import MY_Serial
from plot import MY_3D
import csv

def main():
    h = []
    d = []
    theta = []

    #creating serial object
    s = MY_Serial()
    plotter = MY_3D(h,d,theta)

    if(s.ser.readline().decode('utf-8') == "START?"):
        #scanStarted = s.pyStartScan()

       while (s.ser.readLine().decode('utf-8') != "SCAN_OVER"):

          data = s.rxDataPoint() #of string like "datapoint=h/d/theta"
          if(data.startswith("datapoint=")):
             dataPointStr = data.split('=')[1].strip() #contains h/d/theta
             hdtheta = dataPointStr.split('/')
        
             h.append(float(hdtheta[0]))
             d.append(float(hdtheta[1]))
             theta.append(float(hdtheta[2]))

          if(s.ser.readLine().decode('utf-8') == "LAYER_OVER"):
              layerNum = plotter.plotLayer()
              #csv logic here

              if(layerNum>0):
                s.startNextLayer()


if __name__ == "__main__":
    main()
