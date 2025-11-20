import serial
import time

class MY_Serial:
    
    def __init__(self):

        ser = serial.Serial(
          port = "COM5" ,#change later
          baudrate = 9600,
          timeout = 2,
          write_timeout=2
       )
        self.PY_READY = "PY_READY\n"
        self.NEXTLAYER = "PY_READY_FOR_NEXT_LAYER\n"
        self.ERROR = "ERROR\n"
        self.SCAN_OVER = "SCAN_OVER_ACK\n"

        print("Serial port opened :",self.ser.port)
        time.sleep(3)
        

    #function to recieve data point as a string
    def rxDataPoint(self):
        try :
            line = self.ser.readline().decode('utf-8').strip()
            return line
        
        except Exception as e:
            return "----"

    #function to send ready to start scan flag
    def pyStartScan(self):
        try:
            self.ser.write(self.PY_READY.encode('utf-8'))
            print("Sent Ready message to arduino")
            return True
        
        except Exception as e:
            print("Error while sending start scan message to arduino:",e)
            return False

    def startNextLayer(self):
        try :
            self.ser.write(self.NEXTLAYER.encode('utf-8'))
            print("Sent next layer start message to arduino")
        
        except Exception as e:
            print("Error while sending next layer start message to arduino:",e)

    def scanOverAck(self):
        try :
            self.ser.write(self.scanOverAck.encode('utf-8'))
            print("Sent scan over message to arduino")
        
        except Exception as e:
            print("Error while sending scan over ack message to arduino:",e)

    def errorMsg(self):
        try :
            self.ser.write(self.errorMsg.encode('utf-8'))
            print("Sent error message to arduino")
        
        except Exception as e:
            print("Error while sending error message to arduino:",e)


