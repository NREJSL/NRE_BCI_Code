
from UTIL.event import Event
import os
import json
import time 
import sys
import signal
from threading import Thread
from threading import Event as ThreadEvent
from UTIL.EnvironmentVariables import EnvironmentVariables
import requests
import csv
import numpy as np
from dotenv import load_dotenv
from pylsl import StreamInlet, resolve_stream, StreamOutlet, StreamInfo
# from utils import make_url, make_header, handle_request_errors
# from api_data import configure_stimuli_data, configure_zero_stimuli_data, start_session_data, end_session_data, get_configure_telemetry_data, start_telemetry_data, stimuli_flashing_on_data, stimuli_flashing_off_data, get_stimuli_data_stim_type


class StreamListener():
    def __init__(self, env_var:EnvironmentVariables):
        
        #^Members 
        self.test_flag:bool = False
        self.env_var:EnvironmentVariables = env_var
        
        #^ Threads
        self.classification_thread:Thread = None
        self.correlations_thread:Thread = None
        
        #^Events
        self.stop_thread_event:ThreadEvent = ThreadEvent() 
        self.on_stimuli_classified:Event = Event() 
    
    def _get_test_flag(self)->bool:
       return str(self.env_var.get_var(EnvironmentVariables.TEST_FLAG_KEY)) == "1" 
    
    def start_listening(self):
        
        if(self._get_test_flag()):
            print("Testing UI Only, Won't Listen to streams")
            return
        
        self.stop_thread_event.clear()
        self.classification_thread = Thread(target=self.start_classification_inlet, args=('classification',)).start()
        self.correlations_thread = Thread(target=self.start_correlations_inlet, args=('correlation',)).start()
        

    def stop_listening(self):
        self.stop_thread_event.set()

    def start_classification_inlet(self, postfix):
        directoryPath = os.getenv('DIRECTORY_PATH')
        stream_name = f"{self.env_var.get_var(EnvironmentVariables.PREFIX_KEY)}_{postfix}"
        print(f"Looking for {stream_name}")     
        
        stream = resolve_stream('name', stream_name)
        inlet = StreamInlet(stream[0])
        
        while not self.stop_thread_event.is_set():
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
                #! Raise the stimuli Classified event
                self.on_stimuli_classified.trigger(sample=sample, timestamp=timestamp_str)

                # Uncomment the following code to save the data into a file
                # write_data_to_file(data, timestamp, directoryPath)

                print(f"{postfix} Data: {data}\n")
                print(f"Timestamp: {timestamp:.2f}\n")

        print(f'Thread stopped')
        
    def start_correlations_inlet(self, postfix):
        directoryPath = os.getenv('DIRECTORY_PATH')
        stream_name = f"{self.env_var.get_var(EnvironmentVariables.PREFIX_KEY)}_{postfix}"
        print(f"Looking for {stream_name}")     
        
        stream = resolve_stream('name', stream_name)
        inlet = StreamInlet(stream[0])
        
        while not self.stop_thread_event.is_set():
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

                print(f"{postfix} Data: {data}\n")
                print(f"Timestamp: {timestamp:.2f}\n")

        print(f'Thread stopped')
    # Write data to file
    def write_data_to_file(data, timestamp, directory=None):
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
       
