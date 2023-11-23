from DAQhandler import DAQHandler
from graphics import GraphicsHandler
from scipy.interpolate import interp1d
import pygame
import time
import threading


# global
fps = 0 # the fps counter 
closeThread = False

def main():
    
    global closeThread
    global fps

    pygame.init()
    
    graphics_handler = GraphicsHandler(800, 600)
    AnalogInput = DAQHandler("Dev3/ai0")
    
    DOut = DAQHandler("Dev3/port0/line0")
    
    accepted = False

    while(not accepted):
        AnalogInput.getMax()
        AnalogInput.getMin() 
        print(f"Open: {AnalogInput.maxv} Close: {AnalogInput.minv}")
        accepted = input("Are these values acceptable? (y/n) ") == "y"

    mapper = interp1d([AnalogInput.minv, AnalogInput.maxv], [graphics_handler.x_max,graphics_handler.x_min])
    

    # start voltage reader thread
    voltage_reader_thread = threading.Thread(target=voltage_reader, args=(AnalogInput, DOut,mapper, graphics_handler), daemon=True)
    voltage_reader_thread.start()

    # graphics loop
    clock = pygame.time.Clock()
    FPS = 60
    screen_refresh_count = 0
    screen_start_time = time.time()

    running = True
    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        graphics_handler.draw()

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
def voltage_reader(AnalogInput, DigitalOutput, mapper ,graphics_handler):
    daq_start_time = time.perf_counter_ns()
    daq_readings_count = 0; 
    while not closeThread:
        voltage = AnalogInput.moving_median(100)
        voltage = min(AnalogInput.minv, max(AnalogInput.maxv, voltage))
        x_input = mapper(voltage)
        graphics_handler.updatePosition(x_input)
        DigitalOutput.task.write(bool(graphics_handler.vibrate))
        daq_readings_count += 1
        daq_current_time = time.perf_counter_ns()
        if daq_readings_count % 10 == 0:
            elapsed_time = daq_current_time - daq_start_time
            if elapsed_time != 0:
                frequency = daq_readings_count / elapsed_time / 1e-9
                print(f"Daq: {frequency:.2f} Hz | {fps:.2f} FPS")


if __name__ == "__main__":
    main()