from datetime import datetime
import numpy as np
import platform
import logging
import json
import sys
import os

global config
with open('configs/MP.json', 'r') as f:
    config = json.load(f)

# Define a class for PID control
# , kp=1.0, ki=0.0, kd=0.0, setpoint=0.0
class PID:
    def __init__(self):  # Initialize the PID controller with default parameters
        self.kp = config['PID']['kp']  # Proportional gain
        self.ki = config['PID']['ki']  # Integral gain
        self.kd = config['PID']['kd']  # Derivative gain
        self.setpoint = config['PID']['setpoint']  # Desired setpoint value
        self.prev_error = 0.0  # Previous error value for derivative calculation
        self.integral = 0.0  # Integral term

    def reset(self):  # Reset the PID controller
        self.prev_error = 0.0  # Reset previous error
        self.integral = 0.0  # Reset integral term

    def compute(self, current_value):  # Compute the PID output
        error = self.setpoint - current_value  # Calculate the error
        self.integral += error  # Update the integral term
        derivative = error - self.prev_error  # Calculate the derivative term
        output = (self.kp * error) + (self.ki * self.integral) + (self.kd * derivative)  # Calculate the PID output
        self.prev_error = error  # Update the previous error
        return output  # Return the PID output
