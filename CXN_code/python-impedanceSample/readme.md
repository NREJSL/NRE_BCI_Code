# Python Impedance Sample

  
## Overview

Brief description of the project, including its purpose and key features.  

## Table of Contents

- [Python Impedance Sample](#python-impedance-sample)
  - [Overview](#overview)
  - [Table of Contents](#table-of-contents)
  - [Installation](#installation)
  - [Configuration](#configuration)
  - [Running the App](#running-the-app)
  - [Using the App](#using-the-app)
  - [Code Structure](#code-structure)

## Installation

To run this project, follow these steps:

1.  **Install Python version 3.12:**

```bash
# MacOS commands
# it was found that python3.11 did not work for the MacOS. 
# python3.12 does work however. The commands will recommend using 3.12
python3.12 -m venv venv
source venv/bin/activate # Activate virtual environment
``` 

```bash
#Windows commands
# python3.11 and python3.12 worked equally well for Windows environments. 
python3.11 -m venv venv
venv\Scripts\activate.bat
```

2.  **Install dependencies:**

```bash
pip install -r requirements.txt
```  

## Configuration

Create a .env file in the project directory with the following fields(Or a .env file would be created automatically based on the .env.sample file when this app is launched):

```env
BASE_URL={Device's IP Address}
PORT=5000
EXPERIMENT_NAME_PREFIX=cognixion
EXPERIMENT_NAME_POSTFIX=calculated_impedance
```

You can set the experiment name in the .env file. When you configure a scene, the experiment name is set to what was included in the .env file.

## Running the App

Navigate to the project directory and run:

```bash
python3 controller.py
```

This  command  will  launch  the  GUI  application.

## Using the App

1. Check impedance of shown channels, Ground, and Reference by pressing the "Check All" button. Wait for all values to show up.

2. To switch between EEG channels (1-8) and AUX channels (9-16), press the AUX/EEG toggle button.

3. The function name `start_lsl_streams` starts up at program launch. This starts the impedance data stream into the app.

## Code Structure

controller.py:  Main function; Displays UI code for the app.

api/api_data.py: Contains API request body for end session, dynamic channel impedance and configure telemetry.

api/call_api.py: Contains impedance, end session, and configure telemetry API call functions to call for impedance data for a specified channel and terminating/configuring the data stream.

ui/impedance_frame.py: Contains functions to display impedance/aux circles, check all/toggle buttons, refreshing the UI, and switching between EEG/AUX states visually.

data/impedance_stream.py: Contains functions to start LSL stream, as well as the stream inlet where data is received from the ecosystem.

utils:  Includes  helper  functions  used  within  the  code.

.env:  Configuration  file  containing  environment  variables.