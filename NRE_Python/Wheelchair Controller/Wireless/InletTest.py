#import plotly.graph_objects as go
import numpy as np
#import serial.serialcli
import spkit as sp
from scipy import signal
import pyxdf
from sklearn.cross_decomposition import CCA
import matplotlib.pyplot as plt
from scipy.stats import norm
from pylsl import StreamInlet, resolve_streams
import threading
import time
import serial
import time
#import serial.tools.list_ports
#from adaptiveThreshold import adaptive_thresh_gmm, adaptive_thresh_distance, threshold_maximumApriori
import pandas as pd
#from serial.tools import list_ports
from scipy import interpolate


streams = resolve_streams()
if len(streams) == 0:
    print("Stream 'NRE_LAB' not found.")
else:
    # Create an inlet to pull data from the stream
    #print(StreamInlet(streams[0]))
    for x in range(len(streams)):
        print(streams[x].name())
        if streams[x].name() == 'cognixion_raw_eeg':
            inlet = StreamInlet(streams[x])
            
        #if streams[x].name() == 'NRE_Lab_Neon Gaze':
        #    try:
        #        inlet2 = StreamInlet(streams[x])
        #    except:
        #        None
                # print('EEG Only Mode')
sample_buffer = []  
while True:
    time
    sample, timestamp = inlet.pull_sample()
    
    '''
    try:
        sample2, timestamp2 = inlet2.pull_sample(timeout=1.0)
    except:
        None
        '''
    if sample is not None:
        #print('sample is', sample)
        #print('sample is', sample2)
        #with buffer_lock:
        sample_buffer.append(sample)
        print('sample_buffer is', sample_buffer[-1])
        sample_buffer = []
        