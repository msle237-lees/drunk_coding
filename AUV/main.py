# Import python custom libraries

from modules.NP import NP


# Import python standard libraries
import os
import sys
import time
import socket
import logging
import platform
from datetime import datetime


# Logging configuration
# Create a logger object for the module
# Detect OS platform
system_os = platform.system()

# Dependent on OS, toggle os type flag
if system_os == "Windows":
    os_type = "windows"
elif system_os == "Linux":
    os_type = "linux"
elif system_os == "Darwin":
    os_type = "mac"
else:
    print("Unsupported OS")
    sys.exit()

# Configure log file path and set up the logger
filename = "Logging"
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
logger.info(f"OS: {os_type}")
logger.info(f"Python version: {sys.version}")
logger.info(f"Python executable: {sys.executable}")

import pygame
import numpy as np

# Initialize pygame
pygame.init()

# Loop until a joystick is found
while True:
    joystick_count = pygame.joystick.get_count()
    
    if joystick_count > 0:
        print(f"{joystick_count} joystick(s) found. Using the first one.")
        break
    else:
        print("No joystick found. Retrying in 3 seconds.")
        pygame.time.wait(3000)

conn = NP(socket.AF_INET, socket.SOCK_STREAM)
# connection.bind(('localhost', 9999))
# connection.listen(1)
# conn, addr = connection.accept()
# logger.info(f'Connection from {addr}')
conn.connect(('127.0.0.1', 9999))

# Use the first joystick
joystick = pygame.joystick.Joystick(0)
joystick.init()

for event in pygame.event.get():
    if event.type == pygame.QUIT:
        pygame.quit()
        quit()

data = np.zeros(8)

def map(x : float, in_min : float, in_max : float, out_min : float, out_max : float) -> float:
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

# Main loop
while True:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
    
    # Update joystick data
    joystick.init()
    
    axis2 = map(joystick.get_axis(2), -0.6, 0.6, -1, 1)
    axis3 = map(joystick.get_axis(3), -0.6, 0.6, -1, 1)
    axis5 = joystick.get_button(0)

    data[2] = round(map(joystick.get_axis(1), -0.6, 0.6, -1, 1), 2)
    data[5] = round(map(joystick.get_axis(0), -0.6, 0.6, -1, 1), 2)
    data[6] = round(map(joystick.get_axis(6), -0.6, 0.6, -1, 1), 2)

    if axis5 == 1:
        data[3] = round(axis2, 2)
        data[4] = round(axis3, 2)
    else:
        data[0] = round(axis3, 2)
        data[1] = round(axis2, 2)

    logger.info(f'Data - {data}')

    str_data = f'{data[0]},{data[1]},{data[2]},{data[3]},{data[4]},{data[5]},{data[6]},R'

    conn.send_string_as_bytes(str_data)

    # Pause for a bit to make the output readable
    pygame.time.wait(10)
