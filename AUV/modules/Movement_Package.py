import numpy as np

class Movement_Package:
    """
    \brief Initialize the Movement_Package (MP) class with given parameters.
    
    Handles the creation and manipulation of thruster matrices for either
    real-world or simulation scenarios.

    \param simulation: Determines if the thruster matrix should be set up
                       for a real-world or simulation environment.
    """
    
    def __init__(self, simulation=False):
        """ \brief Constructor for initializing the Movement_Package class.
        
        \param simulation (bool): Determines if thruster matrix is for real-world or simulation.
        """
        # Total number of thrusters
        self.num_thrusters = 8  
        # Degrees of freedom (X, Y, Z, Roll, Pitch, Yaw)
        self.num_dof = 6  
        
        # Thruster angle in degrees
        self.angle_in_degrees = 45  
        # Distance from center of mass to thrusters
        self.distance_from_center = 1.0  
        
        # Convert angle from degrees to radians
        self.angle_in_radians = self.angle_in_degrees * (np.pi / 180)
        
        # Initialize thruster data array
        self.thruster_data = np.zeros(self.num_thrusters)
        
        # Create thruster matrix based on simulation flag
        if simulation:
            self.thruster_matrix = self.create_thruster_matrix_real_world()
        else:
            self.thruster_matrix = self.create_thruster_matrix_simulation()

    def create_thruster_matrix_real_world(self):
        """ \brief Create the thruster matrix for a real-world scenario.
        
        \return np.ndarray: The real-world thruster matrix.
        """
        thruster_matrix = np.zeros((self.num_thrusters, self.num_dof))
        
        # Compute forces and moments for horizontal thrusters
        for i in range(4):
            angle_adjustment = np.pi if i % 2 == 1 else 0
            d = np.array([np.cos(self.angle_in_radians + angle_adjustment), np.sin(self.angle_in_radians + angle_adjustment), 0])
            m = np.array([0, 0, self.distance_from_center * np.sin(self.angle_in_radians + angle_adjustment)])
            thruster_matrix[i, :3] = d
            thruster_matrix[i, 3:] = m

        # Configure vertical thrusters for Z-axis, Roll, and Pitch
        for i in range(4, 8):
            d = np.array([0, 0, 1])
            m = np.array([(-1)**((i - 4) // 2) * self.distance_from_center,  (-1)**((i - 4) % 2) * self.distance_from_center, 0])
            thruster_matrix[i, :3] = d
            thruster_matrix[i, 3:] = m

        return thruster_matrix

    def create_thruster_matrix_simulation(self):
        """ \brief Create the thruster matrix for a simulated scenario.
        
        \return np.ndarray: The simulated thruster matrix.
        """
        thruster_matrix = np.zeros((self.num_thrusters, self.num_dof))
        
        # Compute forces and moments for horizontal thrusters
        for i in range(4):
            angle_adjustment = np.pi if i % 2 == 1 else 0
            d = np.array([np.cos(self.angle_in_radians + angle_adjustment), np.sin(self.angle_in_radians + angle_adjustment), 0])
            m = np.array([0, 0, self.distance_from_center * np.sin(self.angle_in_radians + angle_adjustment)])
            thruster_matrix[i, :3] = d
            thruster_matrix[i, 3:] = m

        # Configure vertical thrusters for Z-axis, Roll, and Pitch
        for i in range(4, 8):
            d = np.array([0, 0, -1])
            m = np.array([(-1)**((i - 4) // 2) * self.distance_from_center,  (-1)**((i - 4) % 2) * self.distance_from_center, 0])
            thruster_matrix[i, :3] = d
            thruster_matrix[i, 3:] = m

        return thruster_matrix

    def update(self, data):
        """ \brief Update thruster outputs based on desired vehicle movements.
        
        \param data (list): List of desired movements in the 6 DOF.
        \return np.ndarray: Updated thruster data.
        """
        data = np.array(data).reshape(-1, 1)
        self.thruster_data = np.dot(self.thruster_matrix, data).flatten()
        return self.thruster_data

    def map_data(self):
        """ \brief Map the thruster outputs to a new range suitable for actuation.
        
        \return np.ndarray: Mapped thruster data.
        """
        in_min, in_max = -1, 1  
        out_min, out_max = 1000, 2000  

        out_data = np.zeros(len(self.thruster_data))
        
        # Map the thruster data to the new range
        for x in range(len(self.thruster_data)):
            out_data[x] = (x - in_min) * (out_max - out_min) // (in_max - in_min) + out_min

        return out_data

    def print_out(self):
        """ \brief Print the current thruster outputs. """
        print(f'Thruster outputs: {self.thruster_data}')

    def run(self):
        """ \brief Main loop to run the program. Takes user input for desired movements. """
        while True:
            data = input("Enter movement data (comma separated, 5 values): ")
            data = data.split(',')
            data = [float(i) for i in data]
            self.update(data)
            self.print_out()

if __name__ == "__main__":
    mp = Movement_Package()
    mp.run()
