# imports
import tkinter as tk
from UTIL.ConfigWindow import ConfigWindow
from UTIL.EnvironmentVariables import EnvironmentVariables

#The High Threshold is the cut off for impedance values that are too large. 
IMPEDANCE_HIGH_THRESHOLD = 200000
# the low Threshold is the cut off for what is considered "good" impedance results
IMPEDANCE_LOW_THRESHOLD = 50000
# the aux threshold is the cut off for impedance values that are too large on the Aux channels
IMPEDANCE_AUX_THRESHOLD = 100000


# Helper function for global variable isEeg (True -> EEG, False -> AUX). Switches display on toggle button click between EEG and AUX.
# params: tk.Tk window, startImpedanceForChannel, stopImpedance, toggleIsEeg, getIsEeg
# tk.Tk window: resetUI parameter
# startImpedanceForChannel: resetUI parameter
# stopImpedance: resetUI parameter
# toggleIsEeg: resetUI parameter
# getIsEeg: resetUI parameter
def handleIsEeg(window, startImpedanceForChannel, stopImpedance, toggleIsEeg, getIsEeg):
    toggleIsEeg()
    resetUI(window, startImpedanceForChannel, stopImpedance, getIsEeg, toggleIsEeg)

# Helper function to create circles using Tkinter
# params: int x, int y, int r, **args
# int x, int y: x and y positions of circle
# int r: radius of circle
# **args: other arguments used to configure circle properties
def createCircle(x, y, r, **args):
    return canvas.create_oval(x - r, y - r, x + r, y + r, **args)

# displays impedance UI circles based on impedance value of a given channel.
# params: float impedance, int channelNumber
# float impedance: impedance value
# int channelNumber: channel number
def displayImpedanceUI(impedance, channelNumber):
    if(impedance <= 0):
        strImpedance = '-'
    else:
        strImpedance = str(round(impedance/1000)) + 'k'
        
    placement = channelNumber if 0 <= channelNumber < 8 else channelNumber - 8
    # set position of circle
    xPos = 1000 * 1/5 * (placement % 4) + (1000 * 1/5)
    yPos = 600 * 1/2 - 100 if placement < 4 else 600 * 1/2 + 100
    
    # default circle/text values.
    impedanceOuterCircle = createCircle(xPos, yPos, 50, fill="white", outline="black")
    impedanceInnerCircle = createCircle(xPos, yPos, 30, fill="white", outline="white")
    channelText = canvas.create_text(xPos, yPos + 75, text="Channel " + str(channelNumber + 1), font=("Arial, 12"), tags=("channelNumber" + str(channelNumber), "channelNumber"), fill="black")
    impedanceText = canvas.create_text(xPos, yPos, text=strImpedance, font=("Arial", 12), fill="black", tags=("impedance" + str(channelNumber), "impedance"))
    
    # change text/circle colour based on channel number and/or impedance value
    if channelNumber < 8:
        if channelNumber == 6:
            canvas.itemconfig(channelText, text = "Ground (G)")
        elif channelNumber == 7:
            canvas.itemconfig(channelText, text = "Reference (R)")
            
        if 1 < impedance < IMPEDANCE_LOW_THRESHOLD:
            canvas.itemconfig(impedanceOuterCircle, fill="green")
        elif IMPEDANCE_LOW_THRESHOLD <= impedance <= IMPEDANCE_HIGH_THRESHOLD:
            canvas.itemconfig(impedanceOuterCircle, fill="red")
        else:
            if impedance != 0:
                canvas.itemconfig(impedanceText, text="LEAD OFF", fill="black")
                canvas.itemconfig(impedanceOuterCircle, fill = "white")
                canvas.itemconfig(impedanceInnerCircle, fill = "white", outline = "white")
    else:
        canvas.itemconfig(impedanceText, fill="black")
        canvas.itemconfig(impedanceOuterCircle, fill = "white")
        canvas.itemconfig(impedanceInnerCircle, fill = "white", outline = "white")
        if impedance > IMPEDANCE_AUX_THRESHOLD:
            canvas.itemconfig(impedanceText, text="LEAD OFF")

# display check all impedance UI button component
# params: startImpedanceForChannel, getIsEeg
# startImpedanceForChannel: on button press, start the impedance lifecycle
# getIsEeg: used to configure startChannel value between EEG (0) and AUX (8)
def displayCheckAll(startImpedanceForChannel, getIsEeg):
    isEeg = getIsEeg()
    startChannel = 0 if isEeg else 8
    checkAllButton = tk.Button(canvas, text="Check All", command=lambda:startImpedanceForChannel(startChannel), highlightbackground="white")
    checkAllButton.place(x=800, y=20, width=150, height = 30)


# Display updated value of given channel
# params: float impedance, int channel
# float impedance: impedance value from impedance stream
# int channel: channel number being checked
def refreshChannel(impedance, channel):
    # Remove components and text from UI
    canvas.delete("impedance" + str(channel), "channelNumber" + str(channel))
    # Update channel with new impedance value
    displayImpedanceUI(impedance, channel)

# Display toggle button between EEG/AUX isEegs based on isEeg. If isEeg == True, display button to switch to AUX isEeg, otherwise display button to switch to EEG isEeg.
# params: tk.Tk window, startImpedanceForChannel, stopImpedance, toggleIsEeg, getIsEeg
# tk.Tk window: handleIsEeg parameter
# startImpedanceForChannel: handleIsEeg parameter
# stopImpedance: handleIsEeg parameter
# getIsEeg: handleIsEeg parameter; used to configure toggleButton text.
# toggleIsEeg: handleIsEeg parameter
def displayToggle(window, startImpedanceForChannel, stopImpedance, toggleIsEeg, getIsEeg):
    isEeg = getIsEeg()
    toggleButton = tk.Button(canvas, text="AUX", command=lambda:handleIsEeg(window, startImpedanceForChannel, stopImpedance, toggleIsEeg, getIsEeg), highlightbackground="white")
    if not isEeg:
        toggleButton.config(text="EEG")
    toggleButton.place(x=50, y = 20, width = 150, height = 30)

# Display end button that stops impedance stream when clicked
def displayEnd(stopImpedance):
    stopImpedanceButton = tk.Button(canvas, text="Stop Impedance", command=stopImpedance, highlightbackground="white")
    stopImpedanceButton.place(width = 150, height = 30, x = 800, y = 550)

# display the Edit .env file button that opens the new window
def display_edit_env_window(window):
    open_env_edit_btn = tk.Button(
        master=canvas,
        text="Edit .env File",
        command=lambda: open_window(window),
        highlightbackground="white")
    open_env_edit_btn.place(width=150, height = 30, x = 50, y = 50)

    
def open_window(window):        
    configWindow = ConfigWindow(env_var= EnvironmentVariables(),root=window)
    skip_keys = [EnvironmentVariables.PORT_KEY]
    configWindow.open_env_config_window(skip_keys=skip_keys)
# Set up user interface for the app.
# params: tk.TK window, startImpedanceForChannel, stopImpedance, getIsEeg, toggleIsEeg
# tk.Tk window: tkinter window that backbones UI
# startImpedanceForChannel: displayToggle and displayCheckAll parameter
# stopImpedance: displayToggle, displayEnd parameter
# getIsEeg: displayToggle, displayCheckAll parameter
# toggleIsEeg: displayToggle parameter
def displayUI(window, startImpedanceForChannel, stopImpedance, getIsEeg, toggleIsEeg):
    global frame
    global canvas
    global appStateText
    frame = tk.Frame(window, width = 1000, height = 600)
    frame.pack()
    canvas = tk.Canvas(frame, width = 1000, height = 600, bg="white")
    canvas.pack()
    # Destroy all old UI components
    for w in canvas.winfo_children():
        w.destroy
    canvas.delete("impedance", "channelNumber")
    # Display UI components
    displayToggle(window, startImpedanceForChannel, stopImpedance, toggleIsEeg, getIsEeg)
    displayCheckAll(startImpedanceForChannel, getIsEeg)
    displayEnd(stopImpedance)
    display_edit_env_window(window)
    appStateText = tk.StringVar()
    updateAppState("Waiting for impedance check...")
    appStateEntry = tk.Entry(canvas,textvariable=appStateText, state='readonly', readonlybackground='white', foreground='black', justify='center', bd=0, highlightthickness=0)
    appStateEntry.place(width=300, x=350, y=20)
    canvas.update()
    isEeg = getIsEeg()
    for i in range(8):
        if isEeg:
            displayImpedanceUI(0, i)
            continue
        displayImpedanceUI(0, i + 8)

# Destroy all components in window and re-generate them.
# params: tk.Tk window, startImpedanceForChannel, stopImpedance, getIsEeg, toggleIsEeg
# tk.Tk window: displayUI parameter
# startImpedanceForChannel: displayUI parameter
# stopImpedance: displayUI parameter
# getIsEeg: displayUI parameter
# toggleIsEeg: displayUI parameter
def resetUI(window, startImpedanceForChannel, stopImpedance, getIsEeg, toggleIsEeg):
    frame.destroy()
    displayUI(window, startImpedanceForChannel, stopImpedance, getIsEeg, toggleIsEeg)

# Updates status to display the state of the app
# params: bool state
# bool state: state of impedance app
def updateAppState(appState: str):
    appStateText.set(appState)
    
