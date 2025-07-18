# imports
from pylsl import StreamInlet, resolve_stream
from threading import Thread, Event
import os
from UTIL.EnvironmentVariables import EnvironmentVariables

class LSLStream(Thread):
    # constructor
    # params: int channel, receivedImpedanceData
    # int channel: channel to retrieve impedance data from
    # receivedImpedanceData: callback to main function
    def __init__(self, channel, receivedImpedanceData, env_var:EnvironmentVariables):
        super().__init__()
        self.env_vars = env_var
        self._stop_event = Event()
        self.channel = channel
        self.receivedImpedanceData = receivedImpedanceData

    # configure and create stream and stream inlet.
    # get channel impedance value and call receivedImpedanceData
    def run(self):
        prefix = self.env_vars.get_var(EnvironmentVariables.EXPERIMENT_PREFIX_KEY)
        postfix = self.env_vars.get_var(EnvironmentVariables.EXPERIMENT_POSTFIX_KEY)
        stream_name = f"{prefix}_{postfix}"
        print(f"Looking for {stream_name}") 
        stream = resolve_stream('name', stream_name)
        inlet = StreamInlet(stream[0])
        inlet.flush()
        while not self._stop_event.is_set():
            sample, timestamp = inlet.pull_sample(timeout=5)
            if self._stop_event.is_set():
                break
            data = float(sample[0])
            timestamp = float(timestamp)
            print("DATA : ", data, "TIMESTAMP : ", timestamp)
            if data:
                self.receivedImpedanceData(data, self.channel)
                break

    # stop the thread by setting the event flag
    def stop(self):
        self._stop_event.set()
