import serial
import time

class MY_Serial:
    
    def __init__(self,port = "COM5",baudrate = 9600,timeout = 2,reconnect_delays=3):
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.reconnect_delays = reconnect_delays
        self.ser = None
        self.connect()

        self.PY_READY = "PY_READY\n"
        self.NEXTLAYER = "PY_READY_FOR_NEXT_LAYER\n"
        self.ERROR = "ERROR\n"
        self.SCAN_OVER = "SCAN_OVER_ACK\n"

    def connect(self):
        while True:
            try:
                if self.ser and getattr(self.ser , "is_open",False):
                    return
                self.ser = serial.Serial(self.port,self.baudrate,self.timeout,write_timeout=1)
                time.sleep(2)
                return
            
            except Exception as e:
                print("Failed to connect to serial port:",e)
                time.sleep(self.reconnect_delays)
    
    def readLine(self):
        try :
            raw = self.ser.readline()
            if not raw:
                return ""
            
            return raw.decode('utf-8',errors='ignore').strip()
        except Exception as e:
            print("Error while reading line from serial:",e)
            
            try:
                self.connect()
            except Exception:
                pass
            return ""

    
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

    def close(self):
        try:
            if self.ser and getattr(self.ser,"is_open",False):
                self.ser.close()

        except Exception as e:
            pass


'''
older method
#function to recieve data point as a string
    def rxDataPoint(self):
        try :
            line = self.ser.readline().decode('utf-8').strip()
            return line
        
        except Exception as e:
            return "----"
'''