from DAQhandler import DAQHandler
from graphics import GraphicsHandler
from scipy.interpolate import interp1d
import pygame
import time
import threading
import nidaqmx

# global
fps = 0 # the fps counter 
closeThread = False

def main():
    
    global closeThread
    global fps

    pygame.init()
    
    graphics_handler = GraphicsHandler(800, 600)
    
    # distance between finger
    AnalogInput = DAQHandler("Dev3/ai0")
    
    # the button
    DigitalInput = nidaqmx.Task()
    DigitalInput.di_channels.add_di_chan("Dev3/port0/line1")

    # the vibration
    DigitalOutput = DAQHandler("Dev3/port0/line0")
    
    accepted = True
    AnalogInput.maxv = 1.7
    AnalogInput.minv = 3.0
    while(not accepted):
        AnalogInput.getMax()
        AnalogInput.getMin() 

        print(f"Open: {AnalogInput.maxv} Close: {AnalogInput.minv}")
        accepted = input("Are these values acceptable? (y/n) ") == "y"

    # the button thread
    DigitalInput.start()
    buttonIsPressed = DigitalInput.read() # initial state
    DigitalInput.stop()
    debounce_time = 0.1  # Adjust the debounce time as needed 

    mapper = interp1d([AnalogInput.minv, AnalogInput.maxv], [graphics_handler.x_max,graphics_handler.x_min])
    
    # stop the task (Analog) for distance between fingers
    AnalogInput.task.stop()
    AnalogInput.task.timing.cfg_samp_clk_timing(800, sample_mode= nidaqmx.constants.AcquisitionType.CONTINUOUS)
    
    daq_start_time = time.perf_counter_ns()
    daq_readings_count = 0
    
    def callbackFunction (task_handle, every_n_samples_event_type, number_of_samples, callback_data):
        nonlocal daq_start_time
        nonlocal daq_readings_count
        voltage = AnalogInput.moving_median(100)
        voltage = min(AnalogInput.minv, max(AnalogInput.maxv, voltage))
        x_input = mapper(voltage)
        # in case 
        graphics_handler.buttonIsPressed = buttonIsPressed
        graphics_handler.updatePosition(x_input)
        daq_readings_count = daq_readings_count + 1
        daq_current_time = time.perf_counter_ns()
        if daq_readings_count % 10 == 0:
            elapsed_time = daq_current_time - daq_start_time
            if elapsed_time != 0:
                frequency = daq_readings_count / elapsed_time / 1e-9
                #print(f"Daq: {frequency:.2f} Hz | {fps:.2f} FPS")
        return 0
    
    AnalogInput.task.register_every_n_samples_acquired_into_buffer_event(1, callbackFunction)
    AnalogInput.task.start()

    last_edge_time = time.time()

    def buttonCallback(task_handle, every_n_samples_event_type, number_of_samples, callback_data):
        
        nonlocal buttonIsPressed, last_edge_time

        button_state = DigitalInput.read()
        current_time = time.time()
        
        time_passed = current_time - last_edge_time
        
        if time_passed > debounce_time:
            if button_state and not buttonIsPressed:
                buttonIsPressed = True
                print("Digital input changed state: Pressed")
                last_edge_time = current_time
            elif not button_state and buttonIsPressed:
                buttonIsPressed = False
                print("Digital input changed state: Released")
                last_edge_time = current_time
            graphics_handler.buttonIsPressed = buttonIsPressed
        return 0
        
    DigitalInput.timing.cfg_change_detection_timing(rising_edge_chan="Dev3/port0/line1",
                                                    falling_edge_chan="Dev3/port0/line1",
                                                    sample_mode=nidaqmx.constants.AcquisitionType.CONTINUOUS)

    DigitalInput.register_every_n_samples_acquired_into_buffer_event(1, buttonCallback)
    DigitalInput.start()

    # graphics loop
    clock = pygame.time.Clock()
    FPS = 80
    screen_refresh_count = 0
    screen_start_time = time.time()

    running = True
    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        graphics_handler.draw()
        DigitalOutput.task.write(bool(graphics_handler.vibrate))

        screen_refresh_count += 1
        screen_current_time = time.time()
        elapsed_time = screen_current_time - screen_start_time
        if(elapsed_time > 1):
            fps = screen_refresh_count / elapsed_time
            screen_refresh_count = 0
            screen_start_time = screen_current_time
        
        clock.tick(FPS)        
    
    closeThread = True
    AnalogInput.close()
    graphics_handler.close()

# runs in different thread


if __name__ == "__main__":
    main()