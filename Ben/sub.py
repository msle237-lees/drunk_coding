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
import pandas as pd

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

def array_to_str(arr):
    """
    Convert a numpy array to a string representation.

    Parameters:
    arr (np.ndarray): The numpy array to be converted.

    Returns:
    str: String representation of the numpy array.
    """
    return np.array2string(arr)


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
            data = array_to_str(data)
            hi.send(data)
            conn.send(hi.recv())

def main():
    # Define and initialize variables
    sensorData = None
    server = NP(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((config['ip'], 9999))
    print('Socket bound and listening')
    logger.info('Socket bound and listening')
    server.listen(5)
    conn, addr = server.accept()
    print(f'Connection accepted from {addr}')
    logger.info(f'Connection accepted from {addr}')

    mp_parent, mp_child = Pipe()
    hi_parent, hi_child = Pipe()

    mp_process = Process(target=run_MP, args=(mp_child,))
    hi_process = Process(target=run_HI, args=(hi_child,))

    print('Processes starting')
    logger.info('Processes started')
    mp_process.start()
    print('MP started')
    logger.info('MP started')
    hi_process.start()
    print('HI started')
    logger.info('HI started')

    i = 0
    columns = ['Controller Data', 'Thruster Data', 'Sensor Data']
    data = pd.DataFrame(columns=columns)

    try:
        while True:
            # Do not recieve data only send to the surface
            controllerData_List = ['0.0,0.0,0.0,0.0,0.0\n',
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
            
            controllerData = controllerData_List[i]

            # Convert the string to a numpy array of floats
            numeric_data = np.array(controllerData.strip().split(','), dtype=float)

            # Send the data to the thrusters after mapping
            mp_parent.send(numeric_data)
            thruster_data = mp_parent.recv()
            logger.info(f'Thruster data sent: {thruster_data}')
            print(f'Thruster data sent: {thruster_data}')

            # Receive data from the sensors and send motor data
            hi_parent.send(thruster_data)
            sensorData = hi_parent.recv()
            logger.info(f'Sensor data received: {sensorData}')
            print(f'Sensor data received: {sensorData}')

            # Append data to DataFrame
            new_row = {
                'Controller Data': controllerData.strip(),
                'Thruster Data': thruster_data.tolist(),
                'Sensor Data': sensorData
            }
            data = data.append(new_row, ignore_index=True)

            # Send sensorData and frame to the surface
            conn.send_string_as_bytes(sensorData)
            logger.info(f'Data sent to surface: {sensorData}')


    except KeyboardInterrupt as e:
        print('Keyboard interrupt detected')
        logger.info('Keyboard interrupt detected')

    # Close the connection and end the program
    conn.close()
    mp_process.join()
    hi_process.join()

    out_data = 'out/{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}-data.csv'
    data.to_csv(out_data)
    logger.info(f'Data Stored in {out_data}')

    logger.info('Connection closed')
    logger.info('Program ended')
    print('Connection closed')
    print('Program ended')
    mp_parent.close()
    hi_parent.close()

if __name__ == "__main__":
    main()