import serial
import numpy as np

#making the serial object
'''ser = serial.Serial(
    port = "COM5" ,#change later
    baudrate = 9600,
    timeout = 5,
    write_timeout=5
)'''

#defining flags
PY_READY = "PY_READY"
NEXTLAYER = "PY_READY_FOR_NEXT_LAYER"
ERROR = "ERROR"
SCAN_OVER = "SCAN_OVER_ACK"

#defining the arryays that hold thhe data
h = []
d = []
theta = []

#

