from modules.Networking_Package import NP
from modules.Controller_Module import Controller
from datetime import datetime

import logging
import socket
import time

import json

# Logging configuration
# Create a logger object for the module
# Configure log file path and set up the logger
filename = "SURFACE"
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
with open('configs/surface.json') as config_file:
    config = json.load(config_file)
logger.info('Config file loaded')

class surface:
    def __init__(self):
        self.server = NP(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((config['ip'], 9998))
        self.server.listen(5)
        self.conn, self.addr = self.server.accept()

        self.controller = Controller()

    def run(self):
        while True:
            data = self.controller.get_data()
            self.conn.send(str(data).encode())
            time.sleep(0.1)

if __name__ == '__main__':
    su = surface()
    su.run()