import tkinter as tk
import os
import json
import time 
import sys
import requests
import csv
from threading import Thread
import numpy as np
from pylsl import StreamInlet, resolve_stream, StreamOutlet, StreamInfo
import signal
from dotenv import load_dotenv
from MVC.view import View
from MVC.controller import Controller 
from MVC.gameModel import GameModel
from MVC.GameSettings import GameSettings
from UTIL.api import API 
from UTIL.streamListener import StreamListener
from UTIL.LeaderBoardManager import LeaderBoardManager
from UTIL.EnvironmentVariables import EnvironmentVariables 

APP_VERSION = "0.5.4"

def main():   
    
    env_var = EnvironmentVariables()

    # When there is no .env file
    try:
        int(env_var.get_var(EnvironmentVariables.ROUNDS_KEY))
    except TypeError:
        env_var = EnvironmentVariables()

    api = API(env_var=env_var)
    game_settings = GameSettings( env_var=env_var )
    view = View(APP_VERSION, env_var=env_var)
    streams = StreamListener(env_var=env_var) 
    leaderBoard = LeaderBoardManager(env_var=env_var)
    
    controller = Controller(
        view=view,
        model=GameModel(),
        api=api,
        streams=streams,
        game_settings=game_settings,
        leader_board=leaderBoard,
        env_vars=env_var )
    
    controller.start_app()
    
    
    
    

if __name__ == "__main__":
    load_dotenv()
    main()