import numpy as np


class MP:
    def __init__(self):
        self.d1x, self.d1y, self.d1z = 0.241, 0.309, 0.03
        self.d2x, self.d2y, self.d2z = 0.117, 0.296, 0.03
        self.theta = np.pi / 4

        self.thruster_data = np.zeros(8)

        self.thruster_config = [
            {'position': [self.d1x, self.d1y, self.d1z], 'orientation': [np.cos(self.theta), np.sin(self.theta), 0]},
            {'position': [-self.d1x, self.d1y, self.d1z], 'orientation': [-np.cos(self.theta), np.sin(self.theta), 0]},
            {'position': [self.d1x, -self.d1y, self.d1z], 'orientation': [np.cos(self.theta), -np.sin(self.theta), 0]},
            {'position': [-self.d1x, -self.d1y, self.d1z], 'orientation': [-np.cos(self.theta), -np.sin(self.theta), 0]},
            {'position': [self.d2x, self.d2y, self.d2z], 'orientation': [0, 0, 1]},
            {'position': [-self.d2x, self.d2y, self.d2z], 'orientation': [0, 0, 1]},
            {'position': [self.d2x, -self.d2y, self.d2z], 'orientation': [0, 0, 1]},
            {'position': [-self.d2x, -self.d2y, self.d2z], 'orientation': [0, 0, 1]}
        ]

        self.thruster_matrix = self.create_thruster_matrix()

    def get_highest_value_column(self):
        """Get the column with the highest sum of absolute values."""
        column_sums = np.sum(np.abs(self.thruster_matrix), axis=0)  # Sum along columns
        max_column_idx = np.argmax(column_sums)  # Get index of max sum
        max_column = self.thruster_matrix[:, max_column_idx]  # Extract that column
        return max_column

    def create_thruster_matrix(self): #fix function naming into correct casing
        thruster_configurations = self.thruster_config
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
        data = np.array(data).reshape(-1, 1)  # Convert the data to a column vector shape (6, 1)
        self.thruster_data = np.dot(self.thruster_matrix, data)  # Multiply the mixing matrix with the data
        self.out_data = self.get_highest_value_column()
        return self.out_data
