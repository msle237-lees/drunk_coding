from modules.Movement_Package import MP
from modules.Hardware_Interface import HI
from modules.Networking_Package import NP
import socket
import numpy as np
import logging
import platform
import sys
from datetime import datetime
import json
from multiprocessing import Process, Pipe

# Logging configuration
# Create a logger object for the module
# Configure log file path and set up the logger
filename = "SUB"
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
with open('configs/sub.json') as config_file:
    config = json.load(config_file)
logger.info('Config file loaded')

def run_MP(conn : Pipe):
    mp = MP()
    while True:
        data = conn.recv()
        if data is not None:
            mp.update(data)
            mp.map_data()
            conn.send(mp.thruster_data)

def run_HI(conn : Pipe):
    hi = HI()
    while True:
        data = conn.recv()
        if data is not None:
            hi.send(data)
            conn.send(hi.recv())

def main():
    # Define and initialize variables
    sensorData = None
    server = NP(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((config['ip'], 9999))
    logger.info('Socket bound and listening')
    server.listen(5)
    conn, addr = server.accept()
    logger.info(f'Connection accepted from {addr}')

    mp_parent, mp_child = Pipe()
    hi_parent, hi_child = Pipe()

    mp_process = Process(target=run_MP, args=(mp_child,))
    hi_process = Process(target=run_HI, args=(hi_child,))

    logger.info('Processes started')
    mp_process.start()
    logger.info('MP started')
    hi_process.start()
    logger.info('HI started')

    while True:
        # Receive data from the socket
        controllerData = conn.recv_string_as_bytes()
        if controllerData == 'q':
            break

        # Parse the data into a numpy array
        controllerData = np.array(controllerData.split(',')).astype(np.float)
        logger.info(f'Controller data received: {controllerData}')

        # Send the data to the thrusters after mapping
        mp_parent.send(controllerData)
        thruster_data = mp_parent.recv()
        logger.info(f'Thruster data sent: {thruster_data}')

        # Receive data from the sensors and send motor data
        hi_parent.send(thruster_data)
        sensorData = hi_parent.recv()
        logger.info(f'Sensor data received: {sensorData}')

        # Send sensorData and frame to the surface
        data = [sensorData]
        conn.sendall(data)

    # Close the connection and end the program
    conn.close()
    mp_process.join()
    hi_process.join()

    logger.info('Connection closed')
    logger.info('Program ended')
    mp_parent.close()
    hi_parent.close()

if __name__ == "__main__":
    main()