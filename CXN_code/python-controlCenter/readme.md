# Python Control Center

  
## Overview

Brief description of the project, including its purpose and key features.  

## Table of Contents

- [Python Control Center](#python-control-center)
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
# python3.11 does not seem to work for MacOS, however, python3.12 does work.
# The commands for mac Terminal will use 3.12
python3.12 -m venv venv
source venv/bin/activate # Activate virtual environment
``` 

```bash
# Windows commands
# python3.11 and python3.12 worked equally well for Windows environments. 
python3.11 -m venv venv
venv\Scripts\activate.bat
```

2.  **Install dependencies:**

```bash
pip install -r requirements.txt
```  

## Configuration

Create a .env file in the project directory with the following fields(Or a .env file would be created automatically based on the .env.sample file when the App is launched):

```env
BASE_URL= Device's IP Address
PORT=5000
EXPERIMENT_NAME_PREFIX=cognixion
DIRECTORY_PATH=C:\PATH\TO\DATA.CSV\DIRECTORY
```

You can set the experiment name in the .env file. When you configure a scene, the experiment name is set to what was included in the .env file.
Make sure DIRECTORY_PATH is set to universal path (C:\PATH\TO\DATA.CSV\DIRECTORY for Windows, /PATH/TO/DATA.CSV/DIRECTORY for macOS) of where you want to save your csv data to.

## Running the App

Navigate to the project directory and run:

```bash
python3 app.py
```

This  command  will  launch  the  GUI  application.

## Using the App

1. Configure the scene by clicking on the Configure button. This will also set the experiment name.

2. The function name `start_lsl_streams` starts up at program launch. Uncomment the LSL streams that you wish to listen for. By default, the Classification stream is enabled only. 

3. Click on Start to begin flashing. The lsl stream data for the chosen stream will start getting displayed.

4. Click on the End button to stop flashing. This will also stop displaying stream data.

## Code Structure

app.py:  Contains  the  UI  code  and  requests  for  configuring  scenes,  starting/ending  sessions,  and  displaying  LSL  data.

api_data.py:  Contains  the  body  for  different  API  requests.

utils:  Includes  helper  functions  used  within  the  code.

.env:  Configuration  file  containing  environment  variables.