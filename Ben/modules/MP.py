import numpy as np

class MP:
    def __init__(self):
        # Define Constants for Easy Modification
        self.num_thrusters = 6
        self.num_dof = 5  # Degrees of freedom (X, Y, Z, Roll, Yaw)
        self.angle_in_degrees = 30  # Angle of thrusters in degrees
        self.distance_from_center = 1.0  # Distance of each thruster from center of mass

        # Convert angle to radians for trigonometric calculations
        self.angle_in_radians = self.angle_in_degrees * (np.pi / 180)

        # Initialize thruster data
        self.thruster_data = np.zeros(self.num_thrusters)

        # Initialize the thruster matrix
        self.thruster_matrix = self.create_thruster_matrix()

    def create_thruster_matrix(self):
        """
        Create a thruster mixing matrix to map thruster forces to vehicle movements.
        """
        # Initialize thruster matrix with zeros
        thruster_matrix = np.zeros((self.num_thrusters, self.num_dof))

        # Calculate the forces and moments for the 4 horizontal thrusters
        for i in range(4):
            d = np.array([np.cos(self.angle_in_radians), np.sin(self.angle_in_radians) * (-1)**(i//2), 0])  # X, Y, Z forces
            m = np.array([0, (-1)**(i//2) * self.distance_from_center * np.sin(self.angle_in_radians)])  # Roll and Yaw moments
            thruster_matrix[i, :3] = d
            thruster_matrix[i, 3:] = m

        # Configure vertical thrusters for Roll
        thruster_matrix[4, 2] = 1  # Vertical thruster up
        thruster_matrix[4, 3:] = [1, 0]  # Roll, but no Yaw
        
        thruster_matrix[5, 2] = 1  # Vertical thruster also up
        thruster_matrix[5, 3:] = [-1, 0]  # Opposite Roll, but no Yaw

        return thruster_matrix

    def update(self, data):
        """
        Update the thruster outputs based on desired vehicle movements.
        """
        data = np.array(data).reshape(-1, 1)  # Convert to column vector
        self.thruster_data = np.dot(self.thruster_matrix, data).flatten()  # Matrix multiplication
        return self.thruster_data
    
    def map_data(self):
        """
        Map the thruster outputs based on desired vehicle movements.
        """
        in_min = -1
        in_max = 1
        out_min = 1000
        out_max = 2000
        out_data = np.zeros(len(self.thruster_data))
        for x in range(len(self.thruster_data)):
            out_data[x] = (x - in_min) * (out_max - out_min) // (in_max - in_min) + out_min
        return out_data
    
    def print_out(self):
        """
        Print the current thruster outputs.
        """
        print(f'Thruster outputs: {self.thruster_data}')

    def run(self):
        """
        Main loop to run the program.
        """
        while True:
            data = input("Enter movement data (comma separated, 5 values): ")
            data = data.split(',')
            data = [float(i) for i in data]
            self.update(data)
            self.print_out()

if __name__ == "__main__":
    mp = MP()
    mp.run()
