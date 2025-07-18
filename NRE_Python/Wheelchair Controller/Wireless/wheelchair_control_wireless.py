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
import serial.tools.list_ports
#from adaptiveThreshold import adaptive_thresh_gmm, adaptive_thresh_distance, threshold_maximumApriori
import pandas as pd
from serial.tools import list_ports
import pandas as pd
from scipy import interpolate

import socket
import time
arduino_ip = '10.0.0.23'  # Replace with your Arduino's IP
arduino_port = 1234



def getReferenceSignals(length, target_freq, samplingRate):
# generate sinusoidal reference templates for CCA for the first and second harmonics
    reference_signals = []
    t = np.arange(0, (length/(samplingRate)), step=1.0/(samplingRate))

    #First harmonics/Fundamental freqeuncy
    reference_signals.append(np.sin(np.pi*2*target_freq*t))
    reference_signals.append(np.cos(np.pi*2*target_freq*t))
    
    #Second harmonics
    reference_signals.append(np.sin(np.pi*4*target_freq*t))
    reference_signals.append(np.cos(np.pi*4*target_freq*t))

    #Third harmonics
    #reference_signals.append(np.sin(np.pi*8*target_freq*t))
    #reference_signals.append(np.cos(np.pi*8*target_freq*t))

    reference_signals = np.array(reference_signals)
    return reference_signals
    
def findCorr(n_components,numpyBuffer,freq):
# Perform Canonical correlation analysis (CCA)

    try:
        # Check for NaN or Inf values
        if np.any(np.isnan(numpyBuffer)) or np.any(np.isinf(numpyBuffer)):
            print("Warning: NaN or Inf values detected in EEG data")
            numpyBuffer = np.nan_to_num(numpyBuffer)
        
        if np.any(np.isnan(freq)) or np.any(np.isinf(freq)):
            print("Warning: NaN or Inf values detected in reference signals")
            freq = np.nan_to_num(freq)

        # Handle zero variance
        X_var = np.var(numpyBuffer, axis=0) # shape (samples, channels)
        freq_temp = freq.reshape(freq.shape[2], freq.shape[1]*freq.shape[0]) #shape (samples, 2*harmonics)
        Y_var = np.var(freq_temp, axis=0)
        '''
        if np.any(X_var < 1e-10) or np.any(Y_var < 1e-10):
            print("Warning: Near-zero variance detected, adding small noise")
            # Add tiny amount of noise to prevent zero variance
            
            if np.any(X_var < 1e-10):
                numpyBuffer = numpyBuffer + np.random.normal(0, 1e-5, numpyBuffer.shape)
            if np.any(Y_var < 1e-10):
                freq = freq + np.random.normal(0, 1e-5, freq.shape)
        '''
        cca = CCA(n_components)
        corr=np.zeros(n_components)
        result=np.zeros((freq.shape)[0])
        
        for freqIdx in range(0,(freq.shape)[0]):
            
            cca.fit(numpyBuffer,freq[freqIdx,:,:].T)
            O1_a,O1_b = cca.transform(numpyBuffer, freq[freqIdx,:,:].T)
            indVal=0
            for indVal in range(0,n_components):
                corr[indVal] = np.corrcoef(O1_a[:,indVal],O1_b[:,indVal])[0,1]

            result[freqIdx] = np.max(corr)

    except Exception as e:
        print(f"Exception in sklearn CCA: {e}")
        return 0.0
    
    return result

def adaptive_thresh_assignClass(thresh0, thresh1, thresh2, predictedClass, thresh_old):
    
    THRESHL = thresh0
    THRESHF = thresh1
    THRESHR = thresh2
    #print('the thresholds')
    #print(THRESHL)
    #print(THRESHF)
    #print(THRESHR)
    #print(thresh_old)

    # make sure no missing threshold value
    if len(THRESHL) == 0:
        THRESHL = thresh_old[0]

    if len(THRESHF) == 0:
        THRESHF = thresh_old[1]
        
    if len(THRESHR) == 0:
        THRESHR = thresh_old[2]

    dist_left = np.abs(predictedClass[0]-THRESHL)
    dist_right = np.abs(predictedClass[2]-THRESHR)
    dist_forward = np.abs(predictedClass[1]-THRESHF)
    all_dist = [dist_left, dist_right, dist_forward]
    direction = ['L', 'F', 'R']
    #print(all_dist[0])
    #print(all_dist[1])
    #print(all_dist[2])

    # select prediction  
    LEFT = 0
    FORWARD = 0
    RIGHT=0
    
    if predictedClass[0]>=THRESHL:
        LEFT = 1
        output = 'L'

    if predictedClass[1]>=THRESHF:
        FORWARD = 1
        output = 'F'

    if predictedClass[2]>=THRESHR:
        RIGHT = 1
        output = 'R'

    all_dist = [x.item() if isinstance(x, np.ndarray) and x.size == 1 else x for x in all_dist]
    #print('HERE', all_dist)

    if (LEFT+RIGHT+FORWARD == 3):
        closest_direction = np.argmin(all_dist)
        output = direction[closest_direction]

    elif (LEFT+RIGHT == 2):
        closest_direction = np.argmin([all_dist[0], all_dist[-1]])
        output = direction[closest_direction]
        
    elif (LEFT+FORWARD == 2):
        closest_direction = np.argmin(all_dist[0:3])
        output = direction[closest_direction]
            
    elif (RIGHT+FORWARD == 2):
        closest_direction = np.argmin(all_dist[1:])
        output = direction[closest_direction]

    elif (LEFT+RIGHT+FORWARD == 0):
        output = 'S'

    return output


def computeCorrCoeff_cca(dataBuffer, frequencies, windowLength, samplingRate, calibration = False, baselineBuffer =[]):
    # previousWindows is the correlation values of the previous 2 windows
    #global filtered_data
    
    if calibration == False:
        dataBuffer_filtered = sp.filter_X(dataBuffer,band=[5, 30], btype='bandpass', order = 4, fs=samplingRate,verbose=0) 
        #filtered_data.append(dataBuffer_filtered) 
        
        #Generate sinusoidal reference templates for all flicker frequencies
        freq = np.empty([len(frequencies), 4, windowLength])

        for i in range(0, 3):
            freq[i, :, :]=getReferenceSignals(dataBuffer_filtered.shape[0], frequencies[i], samplingRate)[:, 0:len(dataBuffer_filtered)]


        #Compute CCA 
        n_components=1
        result = findCorr(n_components,dataBuffer_filtered,freq)

        print('corr values', result)

    elif calibration == True:
        dataBuffer_filtered = sp.filter_X(baselineBuffer,band=[5, 30], btype='bandpass', order = 4, fs=samplingRate,verbose=0) 


        #Generate sinusoidal reference templates for all flicker frequencies
        freq = np.empty([len(frequencies), 4, windowLength])

        for i in range(0, 3):
            freq[i, :, :]=getReferenceSignals(baselineBuffer.shape[0], frequencies[i], samplingRate)[:, 0:len(baselineBuffer)]


        #Compute CCA 
        n_components=1
        resultC = findCorr(n_components,baselineBuffer,freq)
        return [], resultC
    
    return result, []

def threshold(thresh_old, result, previousWindows, setThresh, calibration, method, result1, resultC1,result2, resultC2, result3, resultC3, means_updated, initial_points0, initial_points1, initial_points2,  means1_appended, variance1_appended, means2_appended, variance2_appended, new_data1_0, new_data2_0, new_data1_1, new_data2_1, new_data1_2, new_data2_2, prior_vals_combined, holder0, holder1, holder2, cutoff_thresh, weights):
    ##assign class

    # method 1 - by selecting above 0.5 corr first then the maximum correlation value
    if method == 'basic':
        # weighting the previous windows
        if (previousWindows != None and len(previousWindows[-1])>0):
            print('WEIGHTS')
            weightNm2 = weights[2]
            weightNm1 = weights[1]
            weightN   = weights[0]

            Nm2 = [x * weightNm2 for x in previousWindows[-2]]
            Nm1 = [x * weightNm1 for x in previousWindows[-1]]
            N = [x * weightN for x in result]

            if len(Nm2) <1:
                result_mod = np.nansum([Nm1, N], axis = 0)
                result = result_mod
            else:
                result_mod = np.sum([Nm2, Nm1, N], axis = 0)
                result = result_mod

        directions = ['L', 'F', 'R', 'S']
        if (result[0] > 0.45) or (result[1] > 0.45) or (result[2] > 0.45):
            predictedClass = np.argmax(result)

        else:
            predictedClass = 3

        print(directions[predictedClass])
        return directions[predictedClass]

    # method 2 - adaptive filter 1
    ## must do for every correlation coefficient computed
    if method == 'adaptiveGMM':

        if calibration:
            data_buffer_calib0 = [element[0] for element in result1] # left data
            data_buffer_calib1 = [element[1] for element in result2] # forward data
            data_buffer_calib2 = [element[2] for element in result3] # rigght data
            
            baseline_buffer_calib0 = [element[0] for element in resultC1] 
            baseline_buffer_calib1 = [element[1] for element in resultC2] 
            baseline_buffer_calib2 = [element[2] for element in resultC3] 

            thresh0, means_updated0, initial_points0 = adaptive_thresh_gmm(data_buffer_calib0, baseline_buffer_calib0, calibration = True, means_updated = [], initial_points=[])
            thresh1, means_updated1, initial_points1 = adaptive_thresh_gmm(data_buffer_calib1, baseline_buffer_calib1, calibration = True, means_updated = [], initial_points=[])
            thresh2, means_updated2, initial_points2 = adaptive_thresh_gmm(data_buffer_calib2, baseline_buffer_calib2, calibration = True, means_updated = [], initial_points=[])
            holder0.append(0)
            holder1.append(0)
            holder2.append(0)
        else:
            print('not in calibration anymore')
            data_buffer0 = result[0]
            data_buffer1 = result[1]
            data_buffer2 = result[2]
            means_updated0 = means_updated[0]
            means_updated1 = means_updated[1]
            means_updated2 = means_updated[2]

            # reduce bias due to uneven clusters, do not append the new corr value if the current and the previous 2 have been below the threshold
            if data_buffer0 < thresh_old[0]:
                holder0.append(1)
            else:
                holder0.append(0)
            if data_buffer1 < thresh_old[1]:
                holder1.append(1)
            else:
                holder1.append(0)           
            if data_buffer2 < thresh_old[2]:
                holder2.append(1)
            else:
                holder2.append(0)
            
            #
            #print('this is holder', holder0)

            if means_updated0.size == 0 or initial_points0.size == 0:
                print('Error: must do calibration first')

            elif (holder0[-1] != 1) and (holder0[-2] != 1) and (holder0[-3] != 1):
                thresh0, means_updated0, initial_points0 = adaptive_thresh_gmm(data_buffer0, baseline_buffer_calib =[], calibration = False, means_updated = means_updated0, initial_points=initial_points0)
            else:
                thresh0 = []

            if means_updated1.size == 0 or initial_points1.size == 0:
                print('Error: must do calibration first')

            elif (holder1[-1] != 1) and (holder1[-2] != 1) and (holder1[-3] != 1):
                thresh1, means_updated1, initial_points1 = adaptive_thresh_gmm(data_buffer1, baseline_buffer_calib =[], calibration = False, means_updated = means_updated1, initial_points=initial_points1)
            else:
                thresh1 = []

            if means_updated2.size == 0 or initial_points2.size == 0:
                print('Error: must do calibration first')

            elif (holder2[-1] != 1) and (holder2[-2] != 1) and (holder2[-3] != 1):
                thresh2, means_updated2, initial_points2 = adaptive_thresh_gmm(data_buffer2, baseline_buffer_calib =[], calibration = False, means_updated = means_updated2, initial_points=initial_points2)
            else:
                thresh2 = []

            #################### old #####################
            #if means_updated0.size == 0 or initial_points0.size == 0:
            #    print('Error: must do calibration first')

            #else:
            #    thresh0, means_updated0, initial_points0 = adaptive_thresh_gmm(data_buffer0, baseline_buffer_calib =[], calibration = False, means_updated = means_updated0, initial_points=initial_points0)
        
            #if means_updated1.size == 0 or initial_points1.size == 0:
            #    print('Error: must do calibration first')

            #else:
            #    thresh1, means_updated1, initial_points1 = adaptive_thresh_gmm(data_buffer1, baseline_buffer_calib =[], calibration = False, means_updated = means_updated1, initial_points=initial_points1)

            #if means_updated2.size == 0 or initial_points2.size == 0:
            #    print('Error: must do calibration first')

            #else: 
            #    thresh2, means_updated2, initial_points2 = adaptive_thresh_gmm(data_buffer2, baseline_buffer_calib =[], calibration = False, means_updated = means_updated2, initial_points=initial_points2)


        #print(thresh0)
        #print(thresh1)
        #print(thresh2)
        thresh_new = [thresh0, thresh1, thresh2]
        means_new = [means_updated0, means_updated1, means_updated2] # make sure within each of these array elements the size is 2 

        return means_new, initial_points0, initial_points1, initial_points2, thresh_new, holder0, holder1, holder2

    # method 3 - adaptive filter 2
    if method == 'adaptiveDistance':

        old_data1_0 = new_data1_0
        old_data2_0 = new_data2_0
        old_data1_1 = new_data1_1
        old_data2_1 = new_data2_1
        old_data1_2 = new_data1_2
        old_data2_2 = new_data2_2

        if calibration:
            data_buffer_calib0 = result1[:, 0] # left data
            data_buffer_calib1 = result2[:, 1] # forward data
            data_buffer_calib2 = result3[:, 2] # rigght data
            
            baseline_buffer_calib0 = resultC1[:, 0]
            baseline_buffer_calib1 = resultC2[:, 1]
            baseline_buffer_calib2 = resultC3[:, 2]

            new_mean1_0, new_var1_0, new_mean2_0, new_var2_0, new_data1_0, new_data2_0, thresh0 = adaptive_thresh_distance(data_buffer_calib0, baseline_buffer_calib =baseline_buffer_calib0, calibration = True, new_data1 = [], new_data2 = [], mean1=[], mean2=[], var1=[], var2=[])
            new_mean1_1, new_var1_1, new_mean2_1, new_var2_1, new_data1_1, new_data2_1, thresh1 = adaptive_thresh_distance(data_buffer_calib1, baseline_buffer_calib =baseline_buffer_calib1, calibration = True, new_data1 = [], new_data2 = [], mean1=[], mean2=[], var1=[], var2=[])
            new_mean1_2, new_var1_2, new_mean2_2, new_var2_2, new_data1_2, new_data2_2, thresh2 = adaptive_thresh_distance(data_buffer_calib2, baseline_buffer_calib =baseline_buffer_calib2, calibration = True, new_data1 = [], new_data2 = [], mean1=[], mean2=[], var1=[], var2=[])

        else:
            data_buffer0 = result[0]
            data_buffer1 = result[1]
            data_buffer2 = result[2]
            new_mean1_0, new_mean1_1, new_mean1_2 = means1_appended[0], means1_appended[1], means1_appended[2]
            new_var1_0, new_var1_1, new_var1_2 = variance1_appended[0], variance1_appended[1], variance1_appended[2]
            new_mean2_0, new_mean2_1, new_mean2_2 = means2_appended[0], means2_appended[1], means2_appended[2]
            new_var2_0, new_var2_2, new_var2_2 = variance2_appended[0], variance2_appended[1], variance2_appended[2]

            if means_updated0.size == 0 or initial_points0.size == 0:
                print('Error: must do calibration first')
            else:
                new_mean1_0, new_var1_0, new_mean2_0, new_var2_0, new_data1_0, new_data2_0, thresh0 = adaptive_thresh_distance(data_buffer0, baseline_buffer_calib =[], calibration = False, new_data1 = new_data1_0, new_data2 = new_data2_0, mean1=new_mean1_0, mean2=new_mean2_0, var1=new_var1_0, var2=new_var2_0)
                new_mean1_1, new_var1_1, new_mean2_1, new_var2_1, new_data1_1, new_data2_1, thresh1 = adaptive_thresh_distance(data_buffer1, baseline_buffer_calib =[], calibration = False, new_data1 = new_data1_1, new_data2 = new_data2_1, mean1=new_mean1_1, mean2=new_mean2_1, var1=new_var1_1, var2=new_var2_1)
                new_mean1_2, new_var1_2, new_mean2_2, new_var2_2, new_data1_2, new_data2_2, thresh2 = adaptive_thresh_distance(data_buffer2, baseline_buffer_calib =[], calibration = False, new_data1 = new_data1_2, new_data2 = new_data2_2, mean1=new_mean1_2, mean2=new_mean2_2, var1=new_var1_2, var2=new_var2_2)

        # appending data points over time
        new_data1_0 = np.append(new_data1_0,old_data1_0)
        new_data2_0 = np.append(new_data2_0,old_data2_0)
        new_data1_1 = np.append(new_data1_1,old_data1_1)
        new_data2_1 = np.append(new_data2_1,old_data2_1)
        new_data1_2 = np.append(new_data1_2,old_data1_2)
        new_data2_2 = np.append(new_data2_2,old_data2_2)

        #print(thresh0)
        #print(thresh1)
        #print(thresh2)

        means1_appended = [new_mean1_0, new_mean1_1, new_mean1_2]
        variance1_appended = [new_var1_0, new_var1_1, new_var1_2]
        means2_appended = [new_mean2_0, new_mean2_1, new_mean2_2]
        variance2_appended = [new_var2_0, new_var2_2, new_var2_2]
        thresh_new = [thresh0, thresh1, thresh2]

        return means1_appended, variance1_appended, means2_appended, variance2_appended, thresh_new, new_data1_0, new_data2_0, new_data1_1, new_data2_1, new_data1_2, new_data2_2


    # method 4 - adaptive filter 3
    if method == 'maximumApriori':

        if calibration:
            data_buffer_calib0 = result1[:, 0] # left data
            data_buffer_calib1 = result2[:, 1] # forward data
            data_buffer_calib2 = result3[:, 2] # rigght data
            
            baseline_buffer_calib0 = resultC1[:, 0]
            baseline_buffer_calib1 = resultC2[:, 1]
            baseline_buffer_calib2 = resultC3[:, 2]

            thresh0, means_updated0, initial_points0, prior_vals_combined = threshold_maximumApriori(data_buffer_calib0, means_updated=[], initial_points=[], calibration = True, baseline_buffer_calib =baseline_buffer_calib0, prior_vals_combined=[])
            thresh1, means_updated1, initial_points1, prior_vals_combined = threshold_maximumApriori(data_buffer_calib1, means_updated=[], initial_points=[], calibration = True, baseline_buffer_calib =baseline_buffer_calib1, prior_vals_combined=[])
            thresh2, means_updated2, initial_points2, prior_vals_combined = threshold_maximumApriori(data_buffer_calib2, means_updated=[], initial_points=[], calibration = True, baseline_buffer_calib =baseline_buffer_calib2, prior_vals_combined=[])

        else:
            data_buffer0 = result[0]
            data_buffer1 = result[1]
            data_buffer2 = result[2]

            if means_updated0.size == 0 or initial_points0.size == 0:
                print('Error: must do calibration first')
            else:
                baseline_buffer_calib=[]
                thresh0, means_updated0, initial_points0 = threshold_maximumApriori(data_buffer0, means_updated0, initial_points0, calibration, baseline_buffer_calib, prior_vals_combined)
                thresh1, means_updated1, initial_points1 = threshold_maximumApriori(data_buffer1, means_updated1, initial_points1, calibration, baseline_buffer_calib, prior_vals_combined)
                thresh2, means_updated2, initial_points2 = threshold_maximumApriori(data_buffer2, means_updated2, initial_points2, calibration, baseline_buffer_calib, prior_vals_combined)

        #print(thresh0)
        #print(thresh1)
        #print(thresh2)
        
        thresh_new = [thresh0, thresh1, thresh2]
        means_new = [means_updated0, means_updated1, means_updated2] # make sure within each of these array elements the size is 2 

        return means_new, initial_points0, initial_points1, initial_points2, thresh_new

    # method 5 - set individual thresholds for each direction
    if method == 'manualThresh':
        
        # weighting the previous windows
        if (previousWindows != None):
            weightNm1 = 0.1
            weightNm2 = 0.1
            weightN   = 0.8

            Nm2 = [x * weightNm2 for x in previousWindows[-2]]
            Nm1 = [x * weightNm1 for x in previousWindows[-1]]
            N = [x * weightN for x in result]

            if len(Nm2) <1:
                result_mod = np.sum([Nm1, N], axis = 0)
                result = result_mod
            else:
                result_mod = np.sum([Nm2, Nm1, N], axis = 0)
                result = result_mod

            #predictedClass= np.argmax(result_mod)

            #print(predictedClass)

        if setThresh != None:
            k = 0
            if (result[0] > setThresh[0]):
                predictedClass = 0
                k = k+1
            if (result[1] > setThresh[1]): 
                predictedClass = 1
                k = k+1
            if (result[2] > setThresh[2]):
                predictedClass = 2
                k = k+1
            if k > 1:
                predictedClass = np.argmax(result)
            else:
                predictedClass = None
            
            #print(predictedClass)


    return predictedClass, thresh_old

sample_buffer = []
sample_buffer2 = []

first_buffer = []
buffer_lock = threading.Lock()

def lsl_inlet_thread():
    global sample_buffer
    global sample_buffer2
    global inlet
    global inlet2
    
 
    streams = resolve_streams()
    if len(streams) == 0:
        print("Stream Cognixion Raw data not found.")
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
                    
    while True:
        
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

        

def lsl_ET_inlet_thread():
    global sample_buffer2
    global inlet2
    
 
    streams = resolve_streams()
    if len(streams) == 0:
        print("Stream ET not found.")
    else:
        # Create an inlet to pull data from the stream
        #print(StreamInlet(streams[0]))
        for x in range(len(streams)):
            #print(streams[x].name())
            if streams[x].name() == 'NRE_Lab_Neon Gaze':
                inlet2 = StreamInlet(streams[x])                    
    while True:
        
        sample2, timestamp2 = inlet2.pull_sample()
        if sample2 is not None:
            #print('sample is', sample)
            #print('sample is', sample2)
            #with buffer_lock:
            sample_buffer2.append(sample2)


def calibrate(filePath0, filePath1, filePath2, filePath3):
    # import calibration data, they should all be the same length
    calib_dataLf = filePath0
    calib_dataFf = filePath1
    calib_dataRf = filePath2
    calib_dataNothingf = filePath3

    calib_dataL=[]
    for stream in calib_dataLf:
        #print(stream)
        if stream.get('info').get('name') == ['cognixion_raw_eeg']:
            #print(stream)
            calib_dataL.append(stream.get('time_series'))

    calib_dataL = calib_dataL[0][:, 0:-1]

    calib_dataF = filePath1=[]
    for stream in calib_dataFf:
        #print(stream)
        if stream.get('info').get('name') == ['cognixion_raw_eeg']:
            #print(stream)
            calib_dataF.append(stream.get('time_series'))

    calib_dataF = calib_dataF[0][:, 0:-1]

    calib_dataR=[]
    for stream in calib_dataRf:
        #print(stream)
        if stream.get('info').get('name') == ['cognixion_raw_eeg']:
            #print(stream)
            calib_dataR.append(stream.get('time_series'))

    calib_dataR = calib_dataR[0][:, 0:-1]

    calib_dataNothing=[]
    for stream in calib_dataNothingf:
        #print(stream)
        if stream.get('info').get('name') == ['cognixion_raw_eeg']:
            #print(stream)
            calib_dataNothing.append(stream.get('time_series'))

    calib_dataNothing = calib_dataNothing[0][:, 0:-1]

    # for baseline data randomly select from the other trials to match the number of data points for both target and baseline 
    BaselineL = np.vstack([calib_dataF, calib_dataR, calib_dataNothing])
    BaselineF = np.vstack([calib_dataL, calib_dataR, calib_dataNothing])
    BaselineR = np.vstack([calib_dataF, calib_dataL, calib_dataNothing])

    resultO_append_left = []
    resultCO_append_left = []
    resultO_append_forward = []
    resultCO_append_forward = []
    resultO_append_right = []
    resultCO_append_right = []

    size0 = calib_dataL.shape[0]
    size1 = calib_dataF.shape[0]
    size2 = calib_dataR.shape[0]

    size0B = BaselineL.shape[0]
    size1B = BaselineF.shape[0]
    size2B = BaselineR.shape[0]

    # process calibration data first    
    for i in range(windowLength, min([size0, size1, size2]), step_length):

        resultO, _ = computeCorrCoeff_cca(calib_dataL[(i-windowLength):i, :], frequencies, windowLength, samplingRate, calibration = False, baselineBuffer =BaselineL[(i-windowLength):i, :])
        resultO_append_left.append(resultO)

        resultO, _ = computeCorrCoeff_cca(calib_dataF[(i-windowLength):i, :], frequencies, windowLength, samplingRate, calibration = False, baselineBuffer =BaselineF[(i-windowLength):i, :])
        resultO_append_forward.append(resultO)

        resultO, _ = computeCorrCoeff_cca(calib_dataR[(i-windowLength):i, :], frequencies, windowLength, samplingRate, calibration = False, baselineBuffer =BaselineR[(i-windowLength):i, :])
        resultO_append_right.append(resultO)

    # process calibration data first    
    for i in range(windowLength, min([size0B, size1B, size2B]), step_length):

        _, resultCO = computeCorrCoeff_cca([], frequencies, windowLength, samplingRate, calibration = True, baselineBuffer =BaselineL[(i-windowLength):i, :])
        resultCO_append_left.append(resultCO)

        _, resultCO = computeCorrCoeff_cca([], frequencies, windowLength, samplingRate, calibration = True, baselineBuffer =BaselineF[(i-windowLength):i, :])
        resultCO_append_forward.append(resultCO)

        _, resultCO = computeCorrCoeff_cca([], frequencies, windowLength, samplingRate, calibration = True, baselineBuffer =BaselineR[(i-windowLength):i, :])
        resultCO_append_right.append(resultCO)

    return resultO_append_left, resultCO_append_left,resultO_append_forward, resultCO_append_forward, resultO_append_right, resultCO_append_right

def processing_thread():
    global sample_buffer
    global sample_buffer2
    global ET_track
    global count1
    global count2
    global corr_save
    #global raw_data
    #global filtered_data
    
    count = 0
    global History 
    History = []
    thresh_total0=[]
    thresh_total1=[]
    thresh_total2=[]
    holder1, holder2, holder3=[], [], []
    corr_save = [[],[]]
    while True:
        time.sleep(step_L)  # Every 2 seconds
        print("")
        if(HybridMode == True):
            print("-------Hybrid Mode------")
        elif(HybridMode == False):
            print("------EEG Only Mode-------")
        #print(len(sample_buffer), sample_buffer)
        print(len(sample_buffer))
        #with buffer_lock:
        if len(sample_buffer) > int(250):
            recent_samples = sample_buffer
            #raw_data.append(recent_samples)
            #temp_window=len(sample_buffer)

            dataBuffer = np.array(recent_samples)[:, 0:-1]
            # remove zeros in the data
            for i in range(0, 6):
                data = dataBuffer[:, i]

                if (data == 0).any():
                    print('FOUND ZERO VALUES')

                    # Indices of non-zero and zero elements
                    x_known = np.where(data != 0)[0]
                    y_known = data[data != 0]
                    x_interp = np.where(data == 0)[0]
                    
                    # Create interpolation function
                    f = interpolate.interp1d(x_known, y_known, kind='cubic', fill_value="extrapolate")
                    data[x_interp] = f(x_interp)
                    dataBuffer[:, i] = data
            #dataBuffer = dataBuffer+dataBuffer[::-1, :]
            #print('shape is', dataBuffer.shape)

            threshold_type = 'basic' # or 'adaptiveGMM' or 'adaptive_thresh_distance'
            calibration = False # or true for calibrating adaptive thresholds
            if threshold_type == 'basic':
                #print('IN BASIC')
                thresh_new=[]
                previousWindows = None
                setThresh = None
                means_new=[]
                calibration = False
                cutoff_thresh = 0.4 # correlation value cutoff for classification
                

                dataBufferCORR, _ = computeCorrCoeff_cca(dataBuffer, frequencies, len(dataBuffer), samplingRate, calibration = False, baselineBuffer =[])
                corr_save.append(dataBufferCORR)
                
                
                ########################################################################################################
                weights = [0.7, 0.2,0.1] # previous window weights -- [current, current-1 , current-2]
                #weights = [1, 1, 1]
                previousWindows = [corr_save[-3], corr_save[-2]]
                ############################################################################################################
                predictedClass =  threshold(thresh_new, dataBufferCORR, previousWindows, setThresh, calibration,threshold_type, [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [],cutoff_thresh, weights)
                print('predicted class is ', predictedClass)
                ''''''
                #print(sample_buffer2[-1])
                
                if(sample_buffer2 != [] and HybridMode == True):
                    
                    if(dataBufferCORR[0] > cutoff_thresh):
                        if (sample_buffer2[-1][0] >= 700 and sample_buffer2[-1][0] <= 880) and (sample_buffer2[-1][1] >= 50 and sample_buffer2[-1][1] <= 1200):
                            predictedClass = 'F'
                            print("Hybrid Mode: F")
                        elif (sample_buffer2[-1][0] <= 700 ) and (sample_buffer2[-1][1] <= 1800) :
                            predictedClass = 'L'
                            print("Hybrid Mode: L")
                        elif (sample_buffer2[-1][0] >= 880 ) and (sample_buffer2[-1][1] <= 1800):
                            predictedClass = 'R'
                            print("Hybrid Mode: R")
                    else:
                        predictedClass = 'S'
                        print("Hybrid Mode: S")
                ''''''
                try:                        
                    indices = np.linspace(0, len(sample_buffer2) - 1, num=10, dtype=int)
                    ET_track.append(count2)
                    count2=count2+1
                    for i in indices:
                        #print('sample_buffer2', sample_buffer2[i])
                        
                        ET_track.append(sample_buffer2[i])
                    #ser.write(bytes(predictedClass, encoding='utf-8'))
                except:
                    ET_track.append([0,0])
                
                try:
                    s.sendall(bytes(predictedClass, encoding='utf-8'))
                    #ser.write(bytes(predictedClass, encoding='utf-8'))
                except:
                    print('Arduino : Offline')
                #print(len(sample_buffer))
                sample_buffer2 = []
                History.append(count1)  
                count1=count1+1
                History.append(predictedClass)

                    
            if threshold_type == 'adaptiveGMM':
                print('the count is', count)
                print('adaptiveGMM')

                if count == 0:
                    calibration = True
                else:
                    calibration = False 
                    
                filePath0, _ = pyxdf.load_xdf('C:\\Users\\uwnrelab\\Dalya\\cognixion\\calibration_forTesting\\jun_may_12_calib\\12.xdf')
                filePath1, _ = pyxdf.load_xdf('C:\\Users\\uwnrelab\\Dalya\\cognixion\\calibration_forTesting\\jun_may_12_calib\\10.xdf')
                filePath2, _ = pyxdf.load_xdf('C:\\Users\\uwnrelab\\Dalya\\cognixion\\calibration_forTesting\\jun_may_12_calib\\13.xdf')
                filePath3, _ = pyxdf.load_xdf('C:\\Users\\uwnrelab\\Dalya\\cognixion\\calibration_forTesting\\jun_may_12_calib\\Rest.xdf')

                dataBufferCORR, _ = computeCorrCoeff_cca(dataBuffer, frequencies, windowLength, samplingRate, calibration = False, baselineBuffer =[])
                
                previousWindows = None
                setThresh = None

                if calibration:
                    
                    means_new=[]
                    initial_points0=[]
                    initial_points1=[]
                    initial_points2=[]

                    result0, resultC0, result1, resultC1, result2, resultC2 = calibrate(filePath0, filePath1, filePath2, filePath3)

                    num1 = np.random.randint(0, high=len(result0), size = len(result0))
                    num2 = np.random.randint(0, high=len(result0), size = len(result0))
                    num3 = np.random.randint(0, high=len(result0), size = len(result0))

                    resultC0_a=[]
                    for i in num1:
                        resultC0_a.append(list(resultC0[i]))

                    resultC0 = resultC0_a
                    
                    resultC1_a=[]
                    for i in num2:
                        resultC1_a.append(list(resultC1[i]))

                    resultC1 = resultC1_a

                    resultC2_a=[]
                    for i in num3:
                        resultC2_a.append(list(resultC2[i]))

                    resultC2 = resultC2_a

                    emptyInput =[]
                    thresh_new=[]
                    means_new, initial_points0, initial_points1, initial_points2, thresh_new, holder1, holder2, holder3 =  threshold(thresh_new, emptyInput, previousWindows, setThresh, calibration, threshold_type, result0, resultC0,result1, resultC1, result2, resultC2, [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], holder1, holder2, holder3)
                    thresh_total0.append(thresh_new[0])
                    thresh_total1.append(thresh_new[1])
                    thresh_total2.append(thresh_new[2])

                    holder1.append(0)
                    holder2.append(0)
                    holder3.append(0)

                    count = count+1
                
                result0, resultC0,result1, resultC1, result2, resultC2 = [], [], [], [], [], []

                # use previous threshold to classify the data 
                #print('the mean is', len(thresh_total1))
                try:
                    thresh_total0_mean = np.mean(thresh_total0)
                except ValueError:
                    thresh_total0_mean = np.mean([x for x in thresh_total0 if len(x) > 0])

                try:
                    thresh_total1_mean = np.mean(thresh_total1)
                except ValueError:
                    thresh_total1_mean = np.mean([x for x in thresh_total1 if len(x) > 0])

                try:
                    thresh_total2_mean = np.mean(thresh_total2)
                except ValueError:
                    thresh_total2_mean = np.mean([x for x in thresh_total2 if len(x) > 0])

                output = adaptive_thresh_assignClass(thresh_new[0], thresh_new[1], thresh_new[2], dataBufferCORR, [thresh_total0_mean, thresh_total1_mean, thresh_total2_mean])
                print(output)
                calibration = False

                # to add weights to previous windows
                corr_save.append(dataBufferCORR)
                previousWindows = [corr_save[-2], corr_save[-1]]

                means_new, initial_points0, initial_points1, initial_points2, thresh_new, holder1, holder2, holder3 =  threshold(thresh_new, dataBufferCORR, previousWindows, setThresh, calibration, threshold_type, result0, resultC0,result1, resultC1, result2, resultC2, means_new, initial_points0, initial_points1, initial_points2, [], [], [], [], [], [], [], [], [], [], [], holder1, holder2, holder3)
                thresh_total0.append(thresh_new[0])
                thresh_total1.append(thresh_new[1])
                thresh_total2.append(thresh_new[2])
                #ser.write(bytes(output, encoding='utf-8'))

            if threshold_type == 'adaptive_thresh_distance':
                    
                if count == 0:
                    calibration = True
                else:
                    calibration = False 
                    
                filePath0, _ = pyxdf.load_xdf('C:\\Users\\uwnrelab\\Dalya\\cognixion\\calibration_forTesting\\8.xdf')
                filePath1, _ = pyxdf.load_xdf('C:\\Users\\uwnrelab\\Dalya\\cognixion\\calibration_forTesting\\10.xdf')
                filePath2, _ = pyxdf.load_xdf('C:\\Users\\uwnrelab\\Dalya\\cognixion\\calibration_forTesting\\13.xdf')
                filePath3, _ = pyxdf.load_xdf('C:\\Users\\uwnrelab\\Dalya\\cognixion\\calibration_forTesting\\7.xdf')

                result0, resultC0, result1, resultC1, result2, resultC2 = calibrate(filePath0, filePath1, filePath2, filePath3)


                dataBufferCORR, _ = computeCorrCoeff_cca(dataBuffer, frequencies, windowLength, samplingRate, calibration = False, baselineBuffer =[])

                means_new=[]
                initial_points0=[]
                initial_points1=[]
                initial_points2=[]
                previousWindows = None
                setThresh = None

                if calibration:
                    emptyInput =[]
                    thresh_new=[]
                    means1_appended, variance1_appended, means2_appended, variance2_appended, thresh_new, new_data1_0, new_data2_0, new_data1_1, new_data2_1, new_data1_2, new_data2_2 =  threshold(thresh_new, emptyInput, previousWindows, setThresh, calibration, threshold_type, result0, resultC0,result1, resultC1, result2, resultC2, [], [], [], [], [], [], [], [], [], [], [], [], [], [], [])

                result0, resultC0,result1, resultC1, result2, resultC2 = [], [], [], [], [], []
                
                output = adaptive_thresh_assignClass(thresh_new[0], thresh_new[1], thresh_new[2], dataBufferCORR, np.nanmean(thresh_total))
                print(output)
                
                means_updated=[]
                initial_points0, initial_points1, initial_points2=[], [], []

                means1_appended, variance1_appended, means2_appended, variance2_appended, thresh_new, new_data1_0, new_data2_0, new_data1_1, new_data2_1, new_data1_2, new_data2_2 =  threshold(thresh_new, dataBufferCORR, previousWindows, setThresh, calibration, threshold_type, result0, resultC0,result1, resultC1, result2, resultC2, means_updated, initial_points0, initial_points1, initial_points2,  means1_appended, variance1_appended, means2_appended, variance2_appended, new_data1_0, new_data2_0, new_data1_1, new_data2_1, new_data1_2, new_data2_2, [])
                thresh_total.append(thresh_new)
                #ser.write(bytes(predictedClass, encoding='utf-8'))

            if threshold_type == 'maximumApriori':
                    
                if count == 0:
                    calibration = True
                else:
                    calibration = False 

                filePath0, _ = pyxdf.load_xdf('C:\\Users\\uwnrelab\\Dalya\\cognixion\\calibration_forTesting\\jun_may_12_calib\\8.xdf')
                filePath1, _ = pyxdf.load_xdf('C:\\Users\\uwnrelab\\Dalya\\cognixion\\calibration_forTesting\\jun_may_12_calib\\10.xdf')
                filePath2, _ = pyxdf.load_xdf('C:\\Users\\uwnrelab\\Dalya\\cognixion\\calibration_forTesting\\jun_may_12_calib\\13.xdf')
                filePath3, _ = pyxdf.load_xdf('C:\\Users\\uwnrelab\\Dalya\\cognixion\\calibration_forTesting\\jun_may_12_calib\\7.xdf')
                result0, resultC0, result1, resultC1, result2, resultC2 = calibrate(filePath0, filePath1, filePath2, filePath3)


                dataBufferCORR, _ = computeCorrCoeff_cca(dataBuffer, frequencies, windowLength, samplingRate, calibration = False, baselineBuffer =[])

                means_new=[]
                initial_points0=[]
                initial_points1=[]
                initial_points2=[]
                previousWindows = None
                setThresh = None

                if calibration:
                    emptyInput =[]
                    thresh_new=[]
                    means_new, initial_points0, initial_points1, initial_points2, thresh_new, prior_vals_combined =  threshold(thresh_new, emptyInput, previousWindows, setThresh, calibration, threshold_type, result0, resultC0,result1, resultC1, result2, resultC2, [], [], [], [], [], [], [], [], [], [], [], [], [], [], [])
                    
                result0, resultC0,result1, resultC1, result2, resultC2 = [], [], [], [], [], []
                
                # use previous threshold to classify the data 
                output = adaptive_thresh_assignClass(thresh_new[0], thresh_new[1], thresh_new[2], dataBufferCORR, np.nanmean(thresh_total))
                print(output)

                means_new, initial_points0, initial_points1, initial_points2, thresh_new =  threshold(thresh_new, dataBufferCORR, previousWindows, setThresh, calibration, threshold_type, result0, resultC0,result1, resultC1, result2, resultC2, means_new, initial_points0, initial_points1, initial_points2, [], [], [], [], [], [], [], [], [], [], prior_vals_combined)
                thresh_total.append(thresh_new)
                #ser.write(bytes(predictedClass, encoding='utf-8'))
            #print(len(sample_buffer))
            sample_buffer=sample_buffer[len(sample_buffer)-int(round(step_length*0.25)):len(sample_buffer)] 
            #sample_buffer=[]
            #sample_buffer.clear
            #inlet.flush()
                # Remove the processed samples
            #print(len(sample_buffer))
        else:
            try:
                s.sendall(bytes('S', encoding='utf-8'))
            except:
                print('Arduino : Offline')
    #time.sleep(0.1)


if __name__ == "__main__":
   
    
    #Arduino initialization

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        s.connect((arduino_ip, arduino_port))
    except:
        print("Missing Connection.")


    global History
    global ET_track
    #global raw_data
    #raw_data=[]
    #global filtered_data
    #filtered_data=[]
    ET_track = []
    win_L=2
    step_L=1.75
    windowLength = int(win_L*250)
    step_length = int(step_L*250)
    dataBuffer = np.zeros((windowLength, 6)) # 250 samples, 8 channels
    frequencies = [10,8,9]
    #frequencies = [12,12,12]
    
    
    global HybridMode
    HybridMode = False
    if(HybridMode == True):
        file_prefix='Hybrid_'
    else:
        file_prefix='EEG_'
    
    global count1
    count1=0
    global count2
    count2=0
    samplingRate = 250
    t1 = threading.Thread(target=lsl_inlet_thread, daemon=True)
    t2 = threading.Thread(target=processing_thread, daemon=True)
    t3 = threading.Thread(target=lsl_ET_inlet_thread, daemon=True)

    t1.start()
    t2.start()
    t3.start()


    try:
        while True:
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("Classification",History)
        print("Corrlist",corr_save)
        print("Eye Tracker",ET_track)
        #print(raw_data)
        timestamp = time.strftime("%m-%d-%H-%M-%S")

        # Create filename with timestamp
        filename = f'output_{timestamp}.txt'
        with open(file_prefix+filename, 'w') as f:
            f.write('**Classification' + str(History)+ '**'+'\n')
            f.write('**Correlation' + str(corr_save)+'**'+ '\n')
            f.write('**Eye track vector' + str(ET_track)+ '**'+'\n')
            print('here')
 
            
        print("Stopping threads.")
    '''
    frequencies = [7.5, 11.5, 13]
    windowLength = int(win_L*250)
    step_length = int(0.5*250)
    samplingRate = 250
    #dataBuffer = # give it the data for this window
    setThresh = None# set thresholds
    previousWindows = None # give it the correlation coefficients for the last 2 windows if you want to implement weighted average 


    ## for online testing
    predictedClass = computeCorrCoeff_cca(dataBuffer, frequencies, windowLength, samplingRate, previousWindows = None)

    # for offline testing
    #data,_ =pyxdf.load_xdf("C:\\Users\\lijun\\OneDrive\\Desktop\\Cognixion_data\\jun_may_5\\AR_F")

    y_data=[]
    for stream in data:
        #print(stream)
        if stream.get('info').get('name') == ['cognixion_raw_eeg']:
            #print(stream)
            y_data.append(stream.get('time_series'))

    TotalBuffer = y_data[0][:, 0:-1]
    target_freq = 7.5
    loc_freq = np.where(np.array(frequencies) == target_freq)[0][0]
    results =[]

    # loop through the windows of x seconds
    for i in range(windowLength, len(TotalBuffer), step_length):

        numpyBuffer0 = TotalBuffer[(i-windowLength):i, :]
        predictedClass = computeCorrCoeff_cca(numpyBuffer0, frequencies, windowLength, samplingRate, previousWindows = None)
        results.append(predictedClass)

    # compute accuracy
    print((np.sum(np.array(results) == loc_freq)/len(results))*100, '%') 
        '''