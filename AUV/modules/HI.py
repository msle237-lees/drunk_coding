from datetime import datetime
import numpy as np
import platform
import logging
import serial
import json
import sys
import os

global config
with open('configs/HI.json', 'r') as f:
    config = json.load(f)

# 
class SIM:
    def __init__(self):
        pass

# 
class ARD:
    def __init__(self):
        pass
