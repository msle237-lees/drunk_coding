from modules.NP import NP
from modules.CM import CM
import logging
import cv2
import numpy as np
import socket
from datetime import datetime
import json

# Logging configuration
# Create a logger object for the module
# Configure log file path and set up the logger
filename = "SURFACE"
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
file_handler = logging.FileHandler(f"logs/surface/{filename}_{timestamp}.log")
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
logger.info("Logger created")

# 