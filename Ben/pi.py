from modules.Networking_Package import NP
from datetime import datetime
import logging
import socket
import time
import json
import threading
import pandas as pd

# Logging configuration
# Create a logger object for the module
# Configure log file path and set up the logger
filename = "PI"
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
file_handler = logging.FileHandler(f"logs/{filename}_{timestamp}.log")
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
logger.info("Logger created")

# Log system information
logger.info(f'Date: {datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}')

# Import the config file
with open('configs/pi.json') as config_file:
    config = json.load(config_file)
logger.info('Config file loaded')

# Create the PI Class that allows for control of the sub with either internal controls or external controls
class PI:
    def __init__(self, internal : bool = True):
        self.internal = internal
        self.data = pd.DataFrame(columns=['time', 'x', 'y', 'z', 'roll', 'pitch', 'yaw', 'Sensor_1', 'Sensor_2', 'Sensor_3'])
        
        if internal: # Connect to the TX2
            self.client = NP(socket.AF_INET, socket.SOCK_STREAM)
            self.client.connect((config['ip'], 9999)) # change the ip to the actual ip of the TX2
            logger.info('Connected to TX2')
            print('Connected to TX2')
            
        else: # Connect to the TX2 and the controller
            self.client = NP(socket.AF_INET, socket.SOCK_STREAM)
            self.client.connect((config['ip'], 9999))
            self.controller = NP(socket.AF_INET, socket.SOCK_STREAM)
            self.controller.connect((config['ip-surface'], 9998))
            logger.info('Connected to TX2 and Controller')
            print('Connected to TX2 and Controller')
        
        self.command_list = ['0.0,0.0,0.0,0.0,0.0\n', 
                             '1.0,0.0,0.0,0.0,0.0\n',
                             '-1.0,0.0,0.0,0.0,0.0\n',
                             '0.0,1.0,0.0,0.0,0.0\n',
                             '0.0,-1.0,0.0,0.0,0.0\n',
                             '0.0,0.0,1.0,0.0,0.0\n',
                             '0.0,0.0,-1.0,0.0,0.0\n',
                             '0.0,0.0,0.0,1.0,0.0\n',
                             '0.0,0.0,0.0,-1.0,0.0\n',
                             '0.0,0.0,0.0,0.0,1.0\n',
                             '0.0,0.0,0.0,0.0,-1.0\n']

    def seperate_thread(self):
        while True:
            data = [self.client.recv_string_as_bytes().split(',')]
            self.data.append(data, ignore_index=True)
            print(data)
            time.sleep(0.1)

    def run(self):
        thread = threading.Thread(target=self.seperate_thread)
        thread.start()
        try:
            auto = False
            choice = input('Do you want to control the sub? (y/n)')
            if choice == 'y':
                auto = False
            else:
                auto = True
            while True:
                if auto:
                    self.client.send_string_as_bytes(self.command_list[0]) # Send the stop command
                    time.sleep(1)
                    self.client.send_string_as_bytes(self.command_list[1]) # Send the forward command
                    time.sleep(5)
                    self.client.send_string_as_bytes(self.command_list[2]) # Send the backward command
                    time.sleep(10)
                    self.client.send_string_as_bytes(self.command_list[1]) # Send the forward command
                    time.sleep(5)
                    self.client.send_string_as_bytes(self.command_list[3]) # Send the right command
                    time.sleep(5)
                    self.client.send_string_as_bytes(self.command_list[4]) # Send the left command
                    time.sleep(10)
                    self.client.send_string_as_bytes(self.command_list[3]) # Send the right command
                    time.sleep(5)
                else:
                    data = self.controller.recv_string_as_bytes()
                    if data == 'q':
                        break
                    self.client.send(data)
                    time.sleep(0.1)
                
        except KeyboardInterrupt:
            out_data = f'out/data-{timestamp}.csv'
            self.data.to_csv(out_data)
            logger.info(f'Data Stored in {out_data}')
            logger.info('Keyboard Interrupt')
            self.client.send(self.command_list[0])
            thread.join()
            exit()

if __name__ == '__main__':
    pi = PI()
    pi.run()
