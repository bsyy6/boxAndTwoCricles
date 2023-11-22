import nidaqmx
from statistics import mode, mean
import time
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

    def __init__(self, channel = None , terminal_config = nidaqmx.constants.TerminalConfiguration.RSE , min_val = -10, max_val = 10):        
        
        if channel is None:
            foundDaq = self.init_daq()
        else:
            if(self.checkChannelValidName(channel)):
                self.channel = channel
                foundDaq = True
            else:
                print(f"Invalid channel name. {channel}")
                foundDaq = self.init_daq()
        
        if foundDaq:
            self.task = nidaqmx.Task()
            self.task.ai_channels.add_ai_voltage_chan(self.channel, terminal_config=terminal_config, min_val=min_val, max_val=max_val)
            self.data = [] # for moving fitlers
            print("connected")
        else:
            print("No DAQ found.")

    def init_daq(self):
        '''
        UI to initializes the DAQ
        '''
        if(nidaqmx.system.System.local().devices.device_names):
            print("Devices found: ")
            devices = nidaqmx.system.System.local().devices
            for i, dev in enumerate(devices.device_names):
                # print device and number
                print(f"[{i}] {dev}")
            if len(devices.device_names) == 1:
                selection = "0"
            else:
                selection = input("Please select a device number: ")
                while not (selection.isdigit() and 0 <= int(selection) < len(devices.device_names)):
                    print("Invalid input. Please enter a valid device number.")
                    selection = input("Please select a device number: ")
            selected_device = devices.device_names[int(selection)]
            channels = devices[selected_device].ai_physical_chans.channel_names
            print(f"Channels found in {selected_device} between {channels[0]} up to {channels[-1]}")
            selection = input(f"Please select a channel number [0 to {len(channels)-1}]: ")
            if(selection == ""):
                selection = 0
            else:
                while not (selection.isdigit() and 0 <= int(selection) < len(channels)):
                    print("Invalid input. Please enter a valid channel number.")
                    selection = input("Please select a channel number: ")
            self.channel = channels[int(selection)]
            print(f"Connecting to: {self.channel}")
            return True
        else:
            print("No devices detected.")
            return False
        
    def checkChannelValidName(self, channel):
        '''
        checks if the channel name is valid Dev3/ai0 for example
        '''
        # 1) check it includes a /
        if "/" not in channel:
            return False
        else:
            device_name = channel.split("/")[0]
            return (channel in nidaqmx.system.System.local().devices[device_name].ai_physical_chans.channel_names)
            
    def add_channel(self, channel , terminal_config = nidaqmx.constants.TerminalConfiguration.RSE , min_val = -10, max_val = 10):
        '''
        adds a channel to the task
        '''
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
    
    def moving_mode(self,n):
        self.data.append(self.read_voltage(number_of_samples_per_channel = n//2))
        if len(self.data) > n:
            self.data = self.data[-n]      
        return mode(self.data)
    
    def read_voltage_mean(self, number_of_samples_per_channel):
        '''
        retuns the [MEAN] of n samples.
        '''
        data = self.task.read(number_of_samples_per_channel=number_of_samples_per_channel)
        return mean(data)
    
    def close(self):
        self.task.close()
    
    # in case the object is deleted, attmpet to close the task first
    def __del__(self):
        self.task.close()

    def getMax(self):
        print("please open your hand and press enter")
        input()
        time.sleep(1)
        self.maxv = self.read_voltage_mean(1000)
    
    def getMin(self):
        print("please close your hand and press enter")
        input()
        time.sleep(1)
        self.minv = self.read_voltage_mean(1000)
    
