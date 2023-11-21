from DAQhandler import DAQHandler
from graphics import GraphicsHandler
from scipy.interpolate import interp1d
import pygame
import time
import nidaqmx
def main():
    pygame.init()
    
    daq_handler = DAQHandler("Dev3/ai0")  # Replace with actual channel
    graphics_handler = GraphicsHandler(800, 600)
    
    # ask user for min and max voltage
    device_buffer_size = 10
    device_buffer = bytearray(device_buffer_size)
    # get all devices connected
    if(nidaqmx.system.System.local().devices.device_names):
        print("Devices connected: ")
        devices = nidaqmx.system.System.local().devices
        for i, dev in enumerate(devices.device_names):
            # print device and number
            print(f"[{i}] {dev}")
        selection = input("Please select a device number: ")
        while not (selection.isdigit() and 0 <= int(selection) < len(devices.device_names)):
            print("Invalid input. Please enter a valid device number.")
            selection = input("Please select a device number: ")

        selected_device = devices.device_names[int(selection)]
        print(f"Selected device: {selected_device}")
    else:
        print("No devices connected")
        exit()
        
    


    mapper = interp1d([0.6, 1.8], [0,10])
    readings_count = 0
    
    start_time = time.perf_counter_ns()


    running = True
    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # graphics_handler.draw(voltage)
        voltage = daq_handler.read_voltage_mode(100)
        time.sleep(1)
        # limit voltage to 0.6 to 1.8
        voltage = min(1.8, max(0.6, voltage))
        x_input = mapper(voltage)
        graphics_handler.draw(x_input)
        # print voltage and x_input 
        
        readings_count += 1
        current_time = time.perf_counter_ns()
        if readings_count % 10 == 0:
            elapsed_time = current_time - start_time
            if elapsed_time != 0:
                frequency = readings_count / elapsed_time / 1e-9
                # print(f"Average frequency: {frequency:.2f} Hz Voltage: {x_input:.2f}")

    daq_handler.close()
    graphics_handler.close()

if __name__ == "__main__":
    main()