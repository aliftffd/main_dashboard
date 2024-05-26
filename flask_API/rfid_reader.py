import serial
import threading
import time
from datetime import datetime

class RFIDReader:
    def __init__(self, port, baud_rate, callback):
        self.serial_port = serial.Serial(port, baud_rate)
        self.stop_event = threading.Event()
        self.callback = callback
        self.tag_names = {
            b'\xE2\x00\x20\x23\x12\x05\xEE\xAA\x00\x01\x00\x73': "TAG 1",
            b'\xE2\x00\x20\x23\x12\x05\xEE\xAA\x00\x01\x00\x76': "TAG 2"
        }

    def read_tag(self):
        while not self.stop_event.is_set():
            command = b'\x02\x02\x03\x03\x00\x00\x00'
            self.serial_port.write(command)
            data = self.serial_port.read(26)

            if len(data) == 26:
                for tag, name in self.tag_names.items():
                    if tag in data:
                        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        tag_id = tag.hex()
                        print(f"{name} terdeteksi: {tag_id} pada {timestamp}")
                        self.callback(timestamp, name, tag_id)
                        break
            else:
                print("Tidak ada data diterima atau data tidak lengkap")

            time.sleep(0.1)

    def start(self):
        self.thread = threading.Thread(target=self.read_tag)
        self.thread.start()

    def stop(self):
        self.stop_event.set()
        self.thread.join()
        self.serial_port.close()

    def __del__(self):
        if self.serial_port.is_open:
            self.serial_port.close()
