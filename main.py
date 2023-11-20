import pygame
import nidaqmx
import numpy as np
import time

# Initialize pygame

pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()


# initialize nidaqmx connected to PCIe-6259
task = nidaqmx.Task()
task.ai_channels.add_ai_voltage_chan("Dev3/ai0", terminal_config = nidaqmx.constants.TerminalConfiguration.RSE, min_val = -10, max_val = 10)



cube = pygame.Surface((50, 50))
cube.fill((255, 0, 0))

timestamps = []
readings_count = 0
start_time = time.time()

running = True

running = True

while running:
    voltage = task.read()
    current_time = time.time()

    # Store timestamp of each reading
    timestamps.append(current_time)

    readings_count += 1

    # Check elapsed time every 100 readings
    if readings_count % 100 == 0:
        elapsed_time = current_time - start_time
        if elapsed_time != 0:
            frequency = readings_count / elapsed_time
            print(f"Average frequency: {frequency:.2f} Hz")
    
    # Exit loop after a certain number of readings
    if readings_count >= 1000:
        break
    

task.close()