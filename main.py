from DAQhandler import DAQHandler
from graphics import GraphicsHandler
from scipy.interpolate import interp1d
import pygame
import time
import threading
import matplotlib.pyplot as plt

def main():


    # Initialize Matplotlib plot
    plt.ion()  # Turn on interactive mode for live plotting
    fig, ax = plt.subplots()
    line, = ax.plot([], [], 'b-', label='Voltage')  # Create an empty plot line
    ax.set_xlabel('Time')
    ax.set_ylabel('Voltage')
    ax.legend()

    pygame.init()
    
    graphics_handler = GraphicsHandler(800, 600)
    daq_handler = DAQHandler("Dev3/ai0")
    
    accepted = False
    while(not accepted):
        daq_handler.getMax()
        daq_handler.getMin() 
        print(f"Open: {daq_handler.maxv} Close: {daq_handler.minv}")
        accepted = input("Are these values acceptable? (y/n) ") == "y"

    mapper = interp1d([daq_handler.minv, daq_handler.maxv], [graphics_handler.x_max,graphics_handler.x_min])
    readings_count = 0
    
    start_time = time.perf_counter_ns()




    running = True
    x_data = []  # Initialize empty lists for x and y data
    y_data = []
    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # graphics_handler.draw(voltage)
        #voltage = daq_handler.read_voltage()
        voltage = daq_handler.moving_median(100)
        voltage = min(daq_handler.minv, max(daq_handler.maxv, voltage))
        x_input = mapper(voltage)
        graphics_handler.draw(x_input)

        # Update x and y data lists
        y_data.append(voltage)
        x_data.append(len(x_data)+1)

        readings_count += 1
        current_time = time.perf_counter_ns()
        if readings_count % 10 == 0:
            elapsed_time = current_time - start_time
            if elapsed_time != 0:
                frequency = readings_count / elapsed_time / 1e-9
                print(f"Average frequency: {frequency:.2f} Voltage: {voltage:.2f} X: {x_input:.2f}")

    line.set_data(x_data,y_data)  # Set new data for the plot
    ax.relim()  # Update the limits of the plot
    ax.autoscale_view(True, True, True)  # Autoscale the view
    plt.pause(0.0001)
    
    daq_handler.close()
    graphics_handler.close()

if __name__ == "__main__":
    main()