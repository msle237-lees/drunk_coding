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

class MP:
    def __init__(self):
        self.d = 0.2
        self.theta = np.pi / 4

        self.thruster_data = np.zeros(8)

        self.eight_thruster_config = [
            {'position': [-1 * self.d, self.d, 0], 'orientation': [-np.cos(self.theta), np.sin(self.theta), 0]}, #! idk why it was multiplied by 1 ???
            {'position': [self.d, self.d, 0], 'orientation': [np.cos(self.theta), np.sin(self.theta), 0]},
            {'position': [self.d, -1 * self.d, 0], 'orientation': [np.cos(self.theta), -np.sin(self.theta), 0]},
            {'position': [-1 * self.d, -1 * self.d, 0], 'orientation': [-np.cos(self.theta), np.sin(self.theta), 0]},
            {'position': [-1 * self.d, 0, self.d], 'orientation': [0, 0, 1]},
            {'position': [0, self.d, self.d], 'orientation': [0, 0, 1]},
            {'position': [self.d, 0, self.d], 'orientation': [0, 0, 1]},
            {'position': [0, -1 * self.d, self.d], 'orientation': [0, 0, 1]}
        ]

        self.thruster_matrix = self.create_thruster_matrix()

    def create_thruster_matrix(self): #fix function naming into correct casing
        thruster_configurations = self.eight_thruster_config
        # Initialize mixing matrix
        mixing_matrix = np.zeros((8, 6))

        # Populate mixing matrix based on thruster configurations
        for i, config in enumerate(thruster_configurations):
            r = np.array(config['position'])
            d = np.array(config['orientation'])
            mixing_matrix[i, :3] = d
            mixing_matrix[i, 3:] = np.cross(r, d)

        return mixing_matrix

    def update(self, data):
        self.thruster_data = data * self.thruster_matrix
        return self.thruster_data
