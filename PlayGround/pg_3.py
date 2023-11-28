# trying to make a more comlex callback function
# you can NOT pass an object to the callback function as of today (2021-03-10)
# check this issue
# 
# https://github.com/ni/nidaqmx-python/issues/143
#

# you either call a global variable or use a nested function to access objects




from DAQhandler import DAQHandler
from graphics import GraphicsHandler
from scipy.interpolate import interp1d
import nidaqmx
import pygame
import time

class CustomData:
    def __init__(self, value):
        self.value = value

def main():
    pygame.init()
    print("started")
    graphics_handler = GraphicsHandler(800, 600)
    AnalogInput = DAQHandler("Dev3/ai0")
    AnalogInput.minv = 0
    AnalogInput.maxv = 4
    graphics_handler.x_min = 0
    mapper = interp1d([AnalogInput.minv, AnalogInput.maxv], [graphics_handler.x_max,graphics_handler.x_min])
    AnalogInput.task.start()

    # here I did calibariton stuff

    AnalogInput.task.stop()
    
    time.sleep(4)
    
    x 
    x = [20,30]  # Pass any value or object you need

    print("created callback")
    #print(callback_data.obj1.x_min)   
    # Register the event callback
    AnalogInput.task.timing.cfg_samp_clk_timing(1, sample_mode=nidaqmx.constants.AcquisitionType.CONTINUOUS)
    
   
    def print_new_data(task_handle, every_n_samples_event_type, number_of_samples, callback_data):
        nonlocal x
        print(f"x from callback : {x[1]}")
        x[1] += 1
        return 0
    
   
    # Register the event callback
    AnalogInput.task.register_every_n_samples_acquired_into_buffer_event(1, print_new_data)
    AnalogInput.task.start()
    while True:
        x[1] = x[1]-1
        print(f" x from main : {x[1]}")
        time.sleep(2)
    input("Press Enter to stop reading\n")
    AnalogInput.task.stop()
    AnalogInput.task.close()





# def print_new_data(task_handle, every_n_samples_event_type, number_of_samples,callback_data = callback_data):
#         # Read the newly acquired samples with moving median filter
#         print( callback_data[0].minv)
#         #voltage = min(callback_data[0].minv, max(callback_data[0].maxv, voltage))
#         #x_input = callback_data[2](voltage)
#         #callback_data[1].updatePosition(x_input) # update position on graphics handler
#         # check for daq frequency
#         #callback_data[0] += callback_data[0].daq_readings_count
#         #callback_data[0].daq_current_time = time.perf_counter_ns()
#         # if(callback_data[0].daq_readings_count % 10 == 0):
#         #     elapsed_time = callback_data[0].daq_current_time - callback_data[0].daq_start_time
#         #     if(elapsed_time != 0):
#         #         frequency = callback_data[0].daq_readings_count / elapsed_time / 1e-9
#         #         print(f"Daq: {frequency:.2f} Hz ")
#         return 0

# Create the callback function with the callback_data

if __name__ == "__main__":
    main()