import numpy as np

## Define Constants for Easy Modification ##
num_thrusters = 6
num_dof = 5  # Degrees of freedom (X, Y, Z, Roll, Yaw)
angle_in_degrees = 30  # Angle of thrusters in degrees
distance_from_center = 1.0  # Distance of each thruster from center of mass

# Convert angle to radians for trigonometric calculations
angle_in_radians = angle_in_degrees * (np.pi / 180)

## Function to Create Thruster Mixing Matrix ##
def create_thruster_matrix():
    """
    Create a thruster mixing matrix to map thruster forces to vehicle movements.
    """
    # Initialize thruster matrix with zeros
    thruster_matrix = np.zeros((num_thrusters, num_dof))

    # Calculate the forces and moments for the 4 horizontal thrusters
    for i in range(4):
        d = np.array([np.cos(angle_in_radians), np.sin(angle_in_radians) * (-1)**(i//2), 0])  # X, Y, Z forces
        m = np.array([0, (-1)**(i//2) * distance_from_center * np.sin(angle_in_radians)])  # Roll and Yaw moments
        thruster_matrix[i, :3] = d
        thruster_matrix[i, 3:] = m

    # Configure vertical thrusters for Roll
    thruster_matrix[4, 2] = 1  # Vertical thruster up
    thruster_matrix[4, 3:] = [1, 0]  # Roll, but no Yaw
    
    thruster_matrix[5, 2] = 1  # Vertical thruster also up
    thruster_matrix[5, 3:] = [-1, 0]  # Opposite Roll, but no Yaw

    return thruster_matrix

## Function to Simulate Thrusters Based on Movement Data ##
def simulate_thrusters(movement_data):
    """
    Simulate the thruster outputs based on desired vehicle movements.
    """
    thruster_matrix = create_thruster_matrix()
    movement_data = np.array(movement_data).reshape(-1, 1)  # Convert to column vector
    return np.dot(thruster_matrix, movement_data).flatten()

## Main Script ##
if __name__ == "__main__":
    while True:
        user_input = input("Enter movement data (comma separated, 5 values): ")
        movement_data = list(map(float, user_input.split(',')))

        if len(movement_data) != num_dof:
            print(f"Please enter exactly {num_dof} values.")
            continue

        thruster_outputs = simulate_thrusters(movement_data)
        print(f"Thruster outputs: {thruster_outputs}")
