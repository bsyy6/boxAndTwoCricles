import nidaqmx
import time
import os

# play ground to test stuff
# I found that cf_smap_clk_timing is not accurate enough for what we need, can set the sampling frequency to fixed using it.

def main():
    print("started")
    # start task
    task = nidaqmx.Task()
    task.ai_channels.add_ai_voltage_chan( "Dev3/ai0" ,terminal_config = nidaqmx.constants.TerminalConfiguration.RSE, min_val = -10, max_val = 3)
    task.timing.cfg_samp_clk_timing(0.2, sample_mode= nidaqmx.constants.AcquisitionType.CONTINUOUS)
    task.start()

    # read voltage
    startTime = time.time() 
    timer = startTime  
    Holder = []
    prevRead = 0
    endTime = startTime + 10  # End time is 2 seconds after the start time
    
    
    thisRead = task.read(number_of_samples_per_channel=nidaqmx.constants.READ_ALL_AVAILABLE)
    
    while time.time() < endTime:
    # make read only 2 seconds long
        # if appended a value it should get the time it appended it too
        buffer_size = task.in_stream.avail_samp_per_chan
        print(f"BEFORE Buffer size: {buffer_size}")
        
        thisRead = task.read(number_of_samples_per_channel=1)
        #if(thisRead != prevRead):
        print(f"{(time.time() - startTime)} \t | {thisRead}") 
        
        buffer_size = task.in_stream.avail_samp_per_chan
        print(f"AFTER Buffer size: {buffer_size}")
        #prevRead = thisRead

    task.stop()
    task.close()

if __name__ == "__main__":
    main()