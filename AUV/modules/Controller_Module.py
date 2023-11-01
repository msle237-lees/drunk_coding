import pygame
import numpy as np

class Controller_Module:
    """ 
    \brief The CM (Control Module) class is used to read input data from an RC flight controller and store it as a numpy array.
    
    \details This class utilizes `pygame` for the joystick interface and `NumPy` for data storage.
    
    \param joystick The pygame Joystick object.
    \param data A numpy array that stores joystick data.
    """
    
    def __init__(self, num_of_axis: int = 5):
        """ 
        \brief Initialize the CM object and call the method to initialize the joystick.
        
        \param num_of_axis Number of axes to initialize in the data array. Default is 5.
        """
        self.joystick = None
        self.data = np.zeros(num_of_axis)
        self.init_joystick()

    def init_joystick(self):
        """ 
        \brief Initialize the pygame library and the joystick.
        
        \details This method will keep retrying until a joystick is found.
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
        \brief Update the `data` array with the latest joystick values.
        
        \details This method reads the joystick values and updates the `data` numpy array.
        
        \return data The updated data array.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        self.joystick.init()

        # Collect joystick axis and button data
        joy_data = [round(self.joystick.get_axis(i), 2) for i in range(self.joystick.get_numaxes())]
        joy_data.append([self.joystick.get_button(i) for i in range(self.joystick.get_numbuttons())])
        
        # Update the data array based on joystick inputs
        if joy_data[8][0]:
            self.data[3] = joy_data[2]  # Roll
        else:
            self.data[1] = joy_data[2]  # Y
        self.data[0] = joy_data[3]  # X
        self.data[2] = joy_data[1]  # Z
        self.data[4] = joy_data[0]  # Yaw

        return self.data
    
    def print(self):
        """ 
        \brief Print the current state of the `data` array.
        
        \details Outputs the current values in the `data` array.
        """
        print(f'X: {self.data[0]} | Y: {self.data[1]} | Z: {self.data[2]} | Roll: {self.data[3]} | Yaw: {self.data[4]}')

if __name__ == "__main__":
    cm = Controller_Module()
    while True:
        cm.get_data()
        cm.print()
        pygame.time.wait(10)
