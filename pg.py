import nidaqmx
import time
import os

def main():
    print("started")
    # start task
    task = nidaqmx.Task()
    task.ai_channels.add_ai_voltage_chan( "Dev3/ai0" ,terminal_config = nidaqmx.constants.TerminalConfiguration.RSE, min_val = -10, max_val = 3)
    task.timing.cfg_samp_clk_timing(10, sample_mode= nidaqmx.constants.AcquisitionType.CONTINUOUS)
    task.start()

    # read voltage
    startTime = time.time()  
    timer = startTime  
    Holder = []
    prevRead = 0
    while True:
        # if appended a value it should get the time it appended it too
        thisRead = task.read()
        
        if(thisRead != prevRead):
            
            print(f"{time.time() - startTime} \t | {thisRead}") 
        prevRead = thisRead
        # lenghtOfHolder = len(Holder)
        # Holder.append((timer, task.read()))
        # if(len(Holder)== lenghtOfHolder):
        #     print("*********************NO VALUE ADDED")
        
        # if(len(Holder)-lenghtOfHolder > 1):
        #     print(f"ADDED {len(Holder)-lenghtOfHolder} VALUES AT THE SAME TIME")
        #     time.sleep(10)

        # timer = time.time() - startTime
        
        # if(len(Holder) > 5):
        #     Holder = Holder[-5:]
        # print("===================")
        # for i in range(len(Holder)):
        #     print(f"{Holder[i][0]:.4f} \t| \t| {Holder[i][1] == Holder[i-1] or i == 0}", end="\n")
        # print("",end= "\r")

if __name__ == "__main__":
    main()