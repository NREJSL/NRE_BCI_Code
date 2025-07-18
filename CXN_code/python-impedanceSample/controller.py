# imports
import shutil
import os.path
import tkinter as tk
from ui.impedance_frame import displayUI, refreshChannel, resetUI, updateAppState
# from api.call_api import callImpedanceAPI, callConfigureTelemetryAPI, callEndSessionAPI, callBCIConfigurationAPI
from data.impedance_stream import LSLStream
from dotenv import load_dotenv
from UTIL.EnvironmentVariables import EnvironmentVariables
from api.call_api import API

# define global variables, load/create .env file
error_no_env = "No .env file found. Creating .env using .env.sample file."
error_no_env_sample = "Unable to create .env file as the .env.sample is missing. \nPlease make sure that .env.sample file is present."
load_dotenv()
lslStream = None
isEeg = True
env_var = EnvironmentVariables()

if not os.path.exists('.env') and os.path.exists('.env.sample'):
    print(error_no_env)
    shutil.copyfile('.env.sample','.env')
    env_var = EnvironmentVariables()
elif not os.path.exists('.env') and not os.path.exists('.env.sample'):
    print(error_no_env_sample)

api = API(env_var=env_var)

AppVersion = "1.5.3"

# toggle isEeg between True and False
def toggleIsEeg():
    global isEeg
    isEeg = not isEeg
    stopImpedance()

# Getter function for isEeg variable
def getIsEeg():
    return isEeg

# Upon receiving data, update the UI and if applicable, start the next channel's impedance check
# params: float impedanceData, int currChannel
# float impedanceData: calculated impedance value received from API
# int currChannel: channel from which calculated impedance value is from
def receivedImpedanceData(impedanceData, currChannel):
    refreshChannel(impedanceData, currChannel)
    currChannel += 1
    if 0 <= currChannel <= 5 or 8 <= currChannel <= 15:
        startImpedanceForChannel(currChannel)
    else:
        stopImpedance()

# configures and starts lsl stream and calls the impedance API to get channel impedance values.
# params: int channel
# int channel: channel number to call impedance API on
def startImpedanceForChannel(channel):
    global lslStream
    stopImpedance()
    if channel == 0 or channel == 8:
        api.callConfigureTelemetryAPI()
        api.callBCIConfigurationAPI()
        resetUI(window, startImpedanceForChannel, stopImpedance, getIsEeg, toggleIsEeg)
    updateAppState("Checking Impedance...")
    
    lslStream = LSLStream(channel, receivedImpedanceData, env_var=EnvironmentVariables())
    lslStream.start()
    api.callImpedanceAPI(channel)
        
# stops the impedance stream and kills the thread.
def stopImpedance():
    if lslStream and lslStream.is_alive():
        lslStream.stop()
    api.callEndSessionAPI()
    updateAppState("Impedance Check Complete.")

# main loop
# define window, frame, canvas
# display UI and start LSL stream
window = tk.Tk()
window.title(f"Measure Impedance v{AppVersion}") 

displayUI(window, startImpedanceForChannel, stopImpedance, getIsEeg, toggleIsEeg)

window.mainloop()

