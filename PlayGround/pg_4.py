# able to detect button press and release with debounce of 100msec

import nidaqmx
import time

def main():
    DigitalInput = nidaqmx.Task()
    DigitalInput.di_channels.add_di_chan("Dev3/port0/line1")

    buttonIsPressed = False
    debounce_time = 0.1  # Adjust the debounce time as needed 
    last_edge_time = time.time()
    
    def buttonCallback(task_handle, every_n_samples_event_type, number_of_samples, callback_data):
        
        nonlocal buttonIsPressed, last_edge_time

        button_state = DigitalInput.read()
        current_time = time.time()
        
        time_passed = current_time - last_edge_time
        
        if time_passed > debounce_time:
            if button_state and not buttonIsPressed:
                buttonIsPressed = True
                #print("Digital input changed state: Button_state")
                last_edge_time = current_time
            elif not button_state and buttonIsPressed:
                buttonIsPressed = False
                #print("Digital input changed state: Released")
                last_edge_time = current_time
        return 0
        
    DigitalInput.timing.cfg_change_detection_timing(rising_edge_chan="Dev3/port0/line1",
                                                    falling_edge_chan="Dev3/port0/line1",
                                                    sample_mode=nidaqmx.constants.AcquisitionType.CONTINUOUS)

    DigitalInput.register_every_n_samples_acquired_into_buffer_event(1, buttonCallback)

    DigitalInput.start()
    # DigitalInput.read()
    input("Press Enter to stop buttonIsPressed\n")
    DigitalInput.stop()
    DigitalInput.close()

if __name__ == "__main__":
    main()

