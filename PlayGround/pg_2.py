import nidaqmx
import time


# showing it can read one channel at 200Hz relatively accurately and works with the callback in a different thread.

def main():
    print("started")
    
    # Create a Task
    task = nidaqmx.Task()
    task.ai_channels.add_ai_voltage_chan("Dev3/ai0", terminal_config=nidaqmx.constants.TerminalConfiguration.RSE, min_val=-10, max_val=3)
    startTime = time.time()
    task.timing.cfg_samp_clk_timing(1, sample_mode=nidaqmx.constants.AcquisitionType.CONTINUOUS)
    x = 1
    def print_new_data(task_handle, every_n_samples_event_type, number_of_samples, callback_data = x ):
        # Read the newly acquired samples
        new_data = task.read()
        print(x)
        print(f"Time: {time.time()-startTime:.3f} | Read: {new_data:.1f}")
        return 0 # The function should return an integer
    # Register the event callback for every 10 new samples acquired
    task.register_every_n_samples_acquired_into_buffer_event(1, print_new_data)
    task.start()
    this = None
    while this != 'x':
        print('Running task. Press x to stop.\n')
        time.sleep(5)
    task.stop()
    task.close()
    print("stopped")
    
        

if __name__ == "__main__":
    main()
