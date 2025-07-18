# Python BCI Game

  
## Overview

Brief description of the project, including its purpose and key features.  

## Table of Contents

- [Python BCI Game](#python-bci-game)
  - [Overview](#overview)
  - [Table of Contents](#table-of-contents)
  - [Installation](#installation)
  - [Configuration](#configuration)
  - [Running the App](#running-the-app)
  - [Using the App](#using-the-app)
  - [Code Structure](#code-structure)

## Installation

To run this project, follow these steps:

1.  **Setup Virtual Environment with Python version 3.12:**

```bash
# python3.11 does not seem to work for MacOS, however, python3.12 does work.

# MacOS commands
python3.12 -m venv venv
source venv/bin/activate

# Windows commands
python3.11 -m venv venv
venv\Scripts\activate.bat
```

2.  **Install dependencies:**

```bash
pip install -r requirements.txt
```  

## Configuration

Here we are setting up the .env file. This holds networking information and the game settings. 
Included in the repo is a sample_env.txt file that has some initial settings. We will use this when making the .env file. Open the sample_env.txt file.
A .env file would be created automatically (if none exists) based on the .env.sample file once the BCI Game is launched.

```bash
#Mac
open sample_env.txt
#Windows
start notepad sample_env.txt
```

In your terminal create a .env file and open in editor 
```bash 
#Mac 
touch .env
open .env

#Windows
echo. > .env
start notepad .env
``` 
 
Copy and paste the contents from the sample_env.txt file into the .env file. 
You will now need to replace the BASE_URL's default value. Change it from AAA.BBB.CCC.DDD to the IP address that is shown in the ServerService app.  




### Modify the game settings
In the .env file there are several game settings that can be adjusted: CHANCES, ROUNDS, and LAYOUT
- CHANCES is the number of tries the player has to select the target stimuli in a round. It's default is 5. If it is set to <=0, then it will be set to the default value.
- ROUNDS is the number rounds of play. It's default value is 10. If it is set to <= 0, then it will be set to the default value.l
- LAYOUT is the stimuli configuration that is used in the game. It's default value is 4. It can be set to 4, 8, or 12. If it is not one of these values, it will be set to the default value.


### Other settings 
- OP_SYSTEM is a value used to indicate the os of the computer. It should be set to "Mac" if you are using a Mac and it should be set to "Windows" if you are using a windows machine. This only really affects the audio output. Audio doesn't work on a Windows machine 
- TEST_FLAG is a value used to test the UI. For normal use, leave it as 0. If it is set to 1, api commands will not be sent through to the device



## Running the App

Navigate to the project directory and run:

```bash
python3 app.py
```
This  command  will  launch  the  GUI  application.

## Using the App

there are 4 buttons on the screen 

- Start Game -> This will begin the game with the current settings in the .env file. If you want to make changes to the .env file, you should close and relaunch the app for those to take effect
- End -> This will interrupt the current running game. The results will not be saved
- Leader Board -> This will open the leader Board page where the previous results will be display
- Exit -> This will close the app window and close the listening threads. 

 