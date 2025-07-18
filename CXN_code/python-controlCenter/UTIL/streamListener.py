import csv
import tkinter as tk
import os
from threading import Thread
from threading import Event as ThreadEvent
from pylsl import StreamInlet, resolve_stream
from UTIL.EnvironmentVariables import EnvironmentVariables 

#StreamListener is used to create lsl inlets on Threads to listen to the streams emitted from the Axon-R
class StreamListener:
    
    def __init__(self ,stop_event:ThreadEvent, env_vars:EnvironmentVariables):
        self.stop_event:ThreadEvent = stop_event
        self.env_vars:EnvironmentVariables = env_vars
        
    
    def _start_lsl_inlet(self,postfix): 
        
        prefix = self.env_vars.get_var(EnvironmentVariables.EXPERIMENT_PREFIX_KEY)
        directoryPath = self.env_vars.get_var(EnvironmentVariables.DIRECTORY_PATH_KEY)
        stream_name = f"{prefix}_{postfix}"
        print(f"Looking for {stream_name}")     
        stream = resolve_stream('name', stream_name)
        inlet = StreamInlet(stream[0])
        
        while not self.stop_event.is_set():
            """
                Pull a sample from the inlet and return it.

                Keyword arguments:
                timeout -- The timeout for this operation, if any. (default FOREVER)
                    If this is passed as 0.0, then the function returns only a
                    sample if one is buffered for immediate pickup.

                Returns a tuple (sample,timestamp) where sample is a list of channel
                values and timestamp is the capture time of the sample on the remote
                machine, or (None,None) if no new sample was available.
            """
            sample, timestamp_str = inlet.pull_sample(timeout=5)

            if(sample != None):       
                data = [value for value in sample]
                timestamp = timestamp_str

                # Uncomment the following code to save the data into a file
                # write_data_to_file(data, timestamp, directoryPath)

                print(f"Data: {data}\n")
                print(f"Timestamp: {timestamp:.2f}\n")

        print(f'Thread stopped')


    # Write data to file
    def write_data_to_file(self,data, timestamp, directory=None):
        # Creating writer object to save LSL Stream data in append mode
        # Replace /path/to/file/data.csv with your desired path to save the file

        if not directory:
            directory = os.getcwd()
            print(directory)

        filePath = os.path.join(directory, 'data.csv')
        print(filePath)

        f = open(filePath, 'a')
        writer = csv.writer(f)

        """
        Writing data to file.
        """
        # Prepping the data
        csvdata = []
        for dataitem in data:
            csvdata.append(dataitem)
        csvdata.append(timestamp)
        writer.writerow(csvdata)

        # Close the file
        f.close()

    # LSL Streams automatically start at program launch
    # To listen to more streams, spin up new LSL threads by uncommenting the code below 
    def start_lsl_streams(self):
        self.stop_event.clear()
        # Thread(target=self._start_lsl_inlet, args=('classification',)).start()
        # Thread(target=self._start_lsl_inlet, args=('correlation',)).start()
        Thread(target=self._start_lsl_inlet, args=('raw_eeg',)).start()
        # Thread(target=self._start_lsl_inlet, args=('filtered_eeg',)).start()
        # Thread(target=self._start_lsl_inlet, args=('impedance',)).start()
        # Thread(target=self._start_lsl_inlet, args=('calculated_impedance',)).start()
        # Thread(target=self._start_lsl_inlet, args=('device_health',)).start()
        # Thread(target=self._start_lsl_inlet, args=('service_status',)).start()
        
        # Thread(target=self._start_lsl_inlet, args=('raw_device_attitude',)).start()
        # Thread(target=self._start_lsl_inlet, args=('head_pose',)).start()

    def stop_lsl_streams(self):
        self.stop_event.set()


