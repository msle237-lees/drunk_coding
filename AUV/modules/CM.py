# # CM Class with Pygame and NumPy
#
# This class, `CM`, demonstrates how to get data from an RC flight controller.
# It uses `pygame` for the joystick interface and `NumPy` for data storage.
# The class has methods for initializing the joystick and updating and printing the control data.
#
# ## Dependencies
# - pygame
# - numpy
#
# ## How to Run
# - Initialize a `CM` object and call its `get_data` and `print` methods in a loop.

import pygame
import numpy as np

class CM:
    """
    ## CM (Control Mapping) Class
    
    The `CM` class is used to read input data from an RC flight controller 
    and store it as a numpy array.
    
    ### Attributes
    - `joystick`: The pygame Joystick object.
    - `data`: A numpy array that stores joystick data.
    """
    
    def __init__(self, num_of_axis: int = 6):
        """
        Initialize the CM object and call the method to initialize the joystick.
        
        ### Parameters
        - `num_of_axis`: Number of axes to initialize in the data array. Default is 6.
        """
        self.joystick = None
        self.data = np.zeros(num_of_axis + 1)
        self.init_joystick()

    def init_joystick(self):
        """
        Initialize the pygame library and the joystick.
        
        This method will keep retrying until a joystick is found.
        """
        pygame.init()
        while True:
            joystick_count = pygame.joystick.get_count()
            if joystick_count > 0:
                print(f"{joystick_count} joystick(s) found. Using the first one.")
                break
            else:
                print("No joystick found. Retrying in 3 seconds.")
                pygame.time.wait(3000)
        
        self.joystick = pygame.joystick.Joystick(0)
        self.joystick.init()

    def get_data(self):
        """
        Update the `data` array with the latest joystick values.
        
        ### Returns
        - `data`: The updated data array.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        self.joystick.init()

        axis2 = self.joystick.get_axis(2)
        axis3 = self.joystick.get_axis(3)
        axis5 = self.joystick.get_axis(5)

        self.data[2] = round(self.joystick.get_axis(1), 2)
        self.data[5] = round(self.joystick.get_axis(0), 2)
        self.data[6] = round(self.joystick.get_axis(6), 2)

        if axis5 < 0:
            self.data[3] = round(axis2, 2)
            self.data[4] = round(axis3, 2)
        else:
            self.data[0] = round(axis3, 2)
            self.data[1] = round(axis2, 2)

        return self.data
    
    def print(self):
        """
        Print the current state of the `data` array.
        """
        print(f'X: {self.data[0]} | Y: {self.data[1]} | Z: {self.data[2]} | Roll: {self.data[3]} | Pitch: {self.data[4]} | Yaw: {self.data[5]} | Claw: {self.data[6]}')

if __name__ == "__main__":
    cm = CM()
    while True:
        cm.get_data()
        cm.print()
        pygame.time.wait(10)
