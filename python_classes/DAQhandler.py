import nidaqmx
from statistics import mode
class DAQHandler:
    '''
    This class handles the communication with the NI DAQ.
    
    Defaults:
    terminal configuration is RSE (Referenced Single-Ended)
    min_val is -10
    max_val is 10
    
    Example use:
    read once:
    DAQ = DAQHandler("Dev3/ai0")
    print(DAQ.read_voltage())
    DAQ.close()

    continuous read:
    DAQ = DAQHandler("Dev3/ai0")
    while True:
        print(DAQ.read_voltage())
        # do other stuff
    DAQ.close()

    read the mode of 10 samples at a time:
    DAQ = DAQHandler("Dev3/ai0")
    while True:
        print(DAQ.read_voltage_mode(10))
    DAQ.close()

    read at a minimum frequency (e.g. 100Hz) with some error slack (e.g. +1ms):
    
    DAQ = DAQHandler("Dev3/ai0")
    onTime = True
    frequency = 100
    dt = 1/frequency
    errorSlack = 0.001 # 1ms
    now = time.time()
    
    while onTime:
        # check if on time
        newnow = time.time()
        
        if(newnow - now > dt && time.time() - currentTime < dt + errorSlack )
            onTime = True
        else:
            onTime = False
            print("error: loop took too long")
            break
            
        now = newnow
        print(DAQ.read_voltage())
        
        # do other stuff
        
        # wait for the rest of the time
        if(time.time() - currentTime < dt):
            time.sleep(dt - (time.time() - currentTime))
        else:
            print("error: loop took too long")
            break
    DAQ.close()

    have fun.
    '''
    def __init__(self, channel , terminal_config = nidaqmx.constants.TerminalConfiguration.RSE , min_val = -10, max_val = 10):
        self.channel = channel
        self.task = nidaqmx.Task()
        self.task.ai_channels.add_ai_voltage_chan( channel ,terminal_config = terminal_config, min_val = min_val, max_val = max_val)
        

    def read_voltage(self):
        '''
        simple read function one sample at a time
        '''
        return self.task.read()

    def read_voltage_mode(self, number_of_samples_per_channel):
        '''
        retuns the [MODE] of n samples.
        '''
        data = self.task.read(number_of_samples_per_channel=number_of_samples_per_channel)
        return mode(data)
    
    def read_voltage_mean(self, number_of_samples_per_channel):
        '''
        retuns the [MEAN] of n samples.
        '''
        data = self.task.read(number_of_samples_per_channel=number_of_samples_per_channel)
        return sum(data)/len(data)
    
    def close(self):
        self.task.close()
    
    # in case the object is deleted, attmpet to close the task first
    def __del__(self):
        self.task.close()