# # Pygame RC Flight Controller Example
#
# This example demonstrates how to use the `pygame` library to get data from an RC flight controller.
# It reads the joystick's axes, buttons, and hat switch (D-pad) values, and prints them in a single line for easy reading.
# 
# ## Dependencies
# - pygame
#
# ## How to Run
# 1. Make sure your RC flight controller is connected to your computer.
# 2. Run this script.

import pygame

# Initialize pygame
pygame.init()

# Loop until a joystick is found
while True:
    joystick_count = pygame.joystick.get_count()
    
    if joystick_count > 0:
        print(f"{joystick_count} joystick(s) found. Using the first one.")
        break
    else:
        print("No joystick found. Retrying in 3 seconds.")
        pygame.time.wait(3000)

# Use the first joystick
joystick = pygame.joystick.Joystick(0)
joystick.init()

# Main loop
while True:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
    
    # Update joystick data
    pygame.joystick.Joystick(0).init()
    
    # Initialize the data string
    data_str = "Data: "
    
    # Accumulate joystick axes data
    axes = joystick.get_numaxes()
    axes_data = [f"A{i}:{joystick.get_axis(i):.2f}" for i in range(axes)]
    data_str += " | ".join(axes_data)
    
    # Accumulate joystick buttons data
    buttons = joystick.get_numbuttons()
    buttons_data = [f"B{i}:{joystick.get_button(i)}" for i in range(buttons)]
    data_str += " | " + " | ".join(buttons_data)
    
    # Accumulate joystick hat (D-pad) data
    hats = joystick.get_numhats()
    hats_data = [f"H{i}:{joystick.get_hat(i)}" for i in range(hats)]
    data_str += " | " + " | ".join(hats_data)

    # Print all data in one line
    print(data_str)

    # Pause for a bit to make the output readable
    pygame.time.wait(10)
