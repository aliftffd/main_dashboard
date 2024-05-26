import serial 
import threading 
import time 

class SpeedDetect: 
    def __init__(self,port,baud_rate,callback): 
        self.serial_port = serial.Serial(port,baud_rate)
        self.stop.event = threading.Event()
        self.callback = callback 

    def read_speed(self): 
        while not self.stop_event.is_set(): 
            try: 
                data = self.serial_port.readline().decode("utf-8").strip() # read serial data from sensor 
                flt = float(data)
                timestamp = self.get_current_datetime()
                self.callback(timestamp,flt)
                time.sleep(5)
            except Exception as e: 
                print("Error reading from serial : ")
    
    def get_current_datetime(self):
        now = datetime.now()
        return now.strftime("%Y-%m-%d %H:%M:%S")

    def start(self): 
        self.thread = threading.Thread(target=self.read_speed)
        self.thread.start()
    
    def stop(self): 
        self.stop_event.set()
        self.thread.join()
        self.serial_port.close()\
        
    def __del__(self): 
        if self.serial_port.is_open(): 
            self.serial_port.close()
