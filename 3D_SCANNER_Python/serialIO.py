# serialIO.py
import serial
import time

class MY_Serial:
    def __init__(self, port="COM5", baudrate=9600, timeout=2, reconnect_delay=3):
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.reconnect_delay = reconnect_delay
        self.ser = None
        self.connect()

        # protocol strings we send
        self.PY_READY = "PY_READY\n"
        self.NEXT_LAYER = "PY_READY_FOR_NEXT_LAYER\n"
        self.SCAN_OVER_ACK = "SCAN_OVER_ACK\n"
        self.ERROR = "ERROR\n"

    def connect(self):
        """Try to open serial repeatedly until success (or exception raised externally)."""
        while True:
            try:
                if self.ser and getattr(self.ser, "is_open", False):
                    return
                self.ser = serial.Serial(port=self.port,
                                         baudrate=self.baudrate,
                                         timeout=self.timeout,
                                         write_timeout=1)
                # allow Arduino auto-reset time
                time.sleep(2)
                return
            except Exception as e:
                print(f"[serialIO] connect failed: {e}. Retrying in {self.reconnect_delay}s")
                time.sleep(self.reconnect_delay)

    def readline(self):
        """Safe readline: returns decoded stripped string or '' on no data."""
        try:
            raw = self.ser.readline()
            if not raw:
                return ""
            return raw.decode("utf-8", errors="ignore").strip()
        except Exception as e:
            print("[serialIO] readline error:", e)
            # attempt reconnect
            try:
                self.connect()
            except Exception:
                pass
            return ""

    # methods to send flags
    def pyStartScan(self):
        try:
            self.ser.write(self.PY_READY.encode())
            print("→ Sent:", self.PY_READY.strip())
            return True
        except Exception as e:
            print("[serialIO] pyStartScan write error:", e)
            return False

    def startNextLayer(self):
        try:
            self.ser.write(self.NEXT_LAYER.encode())
            print("→ Sent:", self.NEXT_LAYER.strip())
            return True
        except Exception as e:
            print("[serialIO] startNextLayer write error:", e)
            return False

    def scanOverAck(self):
        try:
            self.ser.write(self.SCAN_OVER_ACK.encode())
            print("→ Sent:", self.SCAN_OVER_ACK.strip())
            return True
        except Exception as e:
            print("[serialIO] scanOverAck write error:", e)
            return False

    def send_error(self):
        try:
            self.ser.write(self.ERROR.encode())
            return True
        except Exception:
            return False

    def close(self):
        try:
            if self.ser and getattr(self.ser, "is_open", False):
                self.ser.close()
        except Exception:
            pass
