import serial
import time

class HI:
    def __init__(self):
        try:
            self.ser = serial.Serial('/dev/ttyACM0', 115200, timeout=1)
            self.ser.flush()
        except serial.SerialException as e:
            print("Serial exception occurred: {}".format(e))

    def send(self, data: str = '1500,1500,1500,1500,1500,1500R'):
        try:
            self.ser.write(data.encode('utf-8'))
        except serial.SerialException as e:
            print("Error sending data: {}".format(e))

    def recv(self):
        """
            Data input should be in the form of: [0-100,0-1000,0-100,0-50]
        """
        try:
            self.data = self.ser.readline().decode('utf-8').rstrip()
            return self.data
        except serial.SerialException as e:
            print("Error receiving data: {}".format(e))
            return None

    def close(self):
        try:
            self.ser.close()
        except serial.SerialException as e:
            print("Error closing serial port: {}".format(e))

    def print_data(self):
        print(self.data)

    def run(self):
        while True:
            self.send()
            print(self.recv())
            time.sleep(1)

if __name__ == "__main__":
    hi = HI()
    hi.run()
