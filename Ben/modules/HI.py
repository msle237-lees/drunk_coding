import serial
import time

class HI:
    def __init__(self):
        self.ser = serial.Serial('/dev/ttyACM0', 115200, timeout=1)
        self.ser.flush()

    def send(self, data : str = '1500,1500,1500,1500,1500,1500R'):
        self.ser.write(data.encode('utf-8'))
    
    def recv(self):
        """
            Data input should be in the form of: [0-100,0-1000,0-100,0-50]
        """
        self.data = self.ser.readline().decode('utf-8').rstrip()
        return self.data
    
    def close(self):
        self.ser.close()

    def print_data(self):
        print(self.data)

    def run(self):
        while True:
            self.send()
            print(self.recv())
            time.sleep(1)
