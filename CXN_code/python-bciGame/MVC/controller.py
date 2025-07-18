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
from MVC.gameModel import GameModel
from MVC.resultsModel import GameStats
from MVC.PlayerScore import GameResults
from MVC.GameSettings import GameSettings
from solvers.Solvers import StatsSolvers
from UTIL.api import API
from UTIL.streamListener import StreamListener
from UTIL.LeaderBoardManager import LeaderBoardManager
from UTIL.EnvironmentVariables import EnvironmentVariables 

class Controller():
    
    def __init__(self, 
                view: View,
                model:GameModel, 
                api: API, 
                streams:StreamListener, 
                game_settings:GameSettings,
                leader_board:LeaderBoardManager,
                env_vars:EnvironmentVariables): 
        #^Members
        self.view:View = view
        self.model:GameModel = model 
        self.api:API =api
        self.streams:StreamListener = streams
        self.game_settings:GameSettings = None 
        self.leader_board:LeaderBoardManager = leader_board
        self.env_vars:EnvironmentVariables = env_vars
        self.skip_keys:list[str] = [EnvironmentVariables.PORT_KEY, EnvironmentVariables.DIRECTORY_PATH_KEY, EnvironmentVariables.POSTFIX_KEY, EnvironmentVariables.TEST_FLAG_KEY]   
        self.last_game_stats:GameStats = None 
        self.subscribe_to_events()
        
        # self.add_fake_scores()
        
    def subscribe_to_events(self): 
        #stream events
        self.streams.on_stimuli_classified.subscribe_handler(self.handle_stimuli_classified)
        #view events
        self.view.on_start_btn_pressed.subscribe_handler(self.handle_start_button_pressed)
        self.view.on_end_btn_pressed.subscribe_handler(self.handle_end_button_pressed)
        self.view.on_leader_board_btn_pressed.subscribe_handler(self.handle_leader_board_button_pressed)
        self.view.on_exit_btn_pressed.subscribe_handler(self.handle_exit_button_pressed)
        self.view.on_configure_game_btn_pressed.subscribe_handler(self.configure_game)
        
        self.view.on_enter_name_btn_pressed.subscribe_handler(self.handler_enter_button_pressed)
        self.view.on_window_close.subscribe_handler(self.handle_window_close)
        
        self.view.on_open_config_btn_pressed.subscribe_handler(self.handle_open_config_pressed)
        self.view.on_save_variables_btn_pressed.subscribe_handler(self.handle_save_var_pressed)
        self.view.on_close_edit_variables_btn_pressed.subscribe_handler(self.handle_close_edit_pressed)
        
    
        #model events
        self.model.on_game_complete.subscribe_handler(self.handle_game_completed)
        self.model.on_round_started.subscribe_handler(self.handle_round_started)
        self.model.on_round_success.subscribe_handler(self.handle_round_success)
        self.model.on_round_failed.subscribe_handler(self.handle_round_failed)
        self.model.on_round_retry.subscribe_handler(self.handle_round_retry)
        
        self.model.on_game_started.subscribe_handler(lambda total_rounds, chances_per_round, game_layout: self.view.toggle_open_config(False))
        self.model.on_game_ended_early.subscribe_handler(lambda: self.view.toggle_open_config(True))
        self.model.on_game_complete.subscribe_handler(lambda game_results: self.view.toggle_open_config(True))
        
        #streams events
        
        #testing connection 
        self.api.on_api_error.subscribe_handler(self.handle_api_error)
         
        #! testing 
        self.view.on_test_btn_pressed.subscribe_handler(self.handle_test_btn)
        
    def start_app(self):
        print("starting app")
        self.view.start_gui()
        
    def configure_game(self):
        print("Configure pressed")
        self.view.toggle_main_buttons(True, "Controller.configure_game")
        self.api.end_session()
        self.api.configure_bci()
        self.api.configure_telemetry()
        self.api.configure_stimuli(layout= int(self.env_vars.get_var(EnvironmentVariables.LAYOUT_KEY))) 
        self.game_settings = GameSettings(env_var=self.env_vars)
        
    #! testing methods
    def handle_test_btn(self, num:int):
        
        if(num == -1):
            self.api.configure_stimuli(layout= int(self.env_vars.get_var(EnvironmentVariables.LAYOUT_KEY))) 
        else:
            self.handle_stimuli_classified([num],0.0)
        
    def add_fake_scores(self):
        
        self.leader_board.add_score(GameStats("blinky", 1,1,1,0.1,1, ""))
        self.leader_board.add_score(GameStats("pinky", 2,2,2,0.2,2 ,"" ))
        self.leader_board.add_score(GameStats("inky",3,3,3,0.3,3,"" ))
        self.leader_board.add_score(GameStats("clyde",4,4,4,0.4,4,"" ))
        
    #^ Event handlers - API         
    def handle_api_error(self, error_msg, api_method):
        print("Controller.handle_api_error")
        self.view.toggle_main_buttons(False, "Controller.handle_api_error") 
        self.view.clear_round_info()
        self.model.end_game_early() 
    
    #^ Event Handlers - streams
    def handle_stimuli_classified(self, sample, timestamp ):
        self.model.input_stimuli_id(sample[0])
        
    #^ Region: Button Handlers
    def handle_start_button_pressed(self):
        self.streams.start_listening()
        self.game_settings = GameSettings(env_var=self.env_vars)
        self.model.start_game(self.game_settings)
        
    def handle_end_button_pressed(self):
        self.view.clear_round_info()
        self.model.end_game_early()
        self.api.end_session()
    
    def handle_leader_board_button_pressed(self):
        scores = self.leader_board.get_leaderboard()
        self.view.open_leader_board_page(game_stats=None, leaderboard_scores=scores)
        
    def handle_exit_button_pressed(self):
        self.api.on_api_error.unsubscribe_handler(self.handle_api_error)
        
        try:
            self.streams.stop_listening() 
            self.api.end_session()
        except Exception as e:
            print(f"An Error occur when closing the app: {e}")
            
        self.view.close()
        sys.exit()
    
    def handle_window_close(self, root): 
        self.handle_exit_button_pressed()
        
    def handler_enter_button_pressed(self, name:str):
        self.view.close_leaderboard() 
        
        self.last_game_stats.set_name(name)
        self.leader_board.add_score(self.last_game_stats)
        
        scores = self.leader_board.get_leaderboard()
        self.view.open_leader_board_page(game_stats=None, leaderboard_scores=scores)
    
    def handle_open_config_pressed(self):
        self.view.open_app_configuration_screen(self.skip_keys)
        
    def handle_save_var_pressed(self,entries):
        #Saves changes to the .env
        data = {}
        for key, value in entries.items(): 
            
            v_str = value.get()
            
            #check if it is an ipv6 address
            if key == EnvironmentVariables.BASE_URL_KEY and ":" in v_str:
                if not (v_str[0] == "[" and v_str[-1]) == "]":
                    v_str = "{}{}{}".format("[",v_str,"]")
                        
                     
            print(f"{key},{v_str}")   
            
            data[key] = v_str
            
        self.env_vars.save_new_values(data)    
        
        self.handle_close_edit_pressed()
        self.view.toggle_main_buttons(False, "Controller.handle_save_var_pressed")    
          
    #calls close on the Config Screen         
    def handle_close_edit_pressed(self):
        self.view.close_config_screen()
        
        
    #^ Event Handlers - Model
    def handle_target_changed(self, new_target:int):
        self.view.set_new_target(new_target)
    
    def handle_round_started(self, total_rounds:int, current_round:int, chances_left:int, target:int):
        self.view.set_round_info(
            total_rounds=total_rounds, 
            current_round=current_round, 
            target_stimuli=target, 
            chances_remaining=chances_left)
        self.api.start_session()
    
    def handle_game_completed(self, game_results:GameResults):        
        self.api.end_session() 
        #calculate game stats
        solver = StatsSolvers()
        self.last_game_stats = solver.get_game_stats(game_results)
        leaderboard_scores = self.leader_board.get_leaderboard()
        #* Opening leader page 
        self.view.open_leader_board_page(game_stats=self.last_game_stats, leaderboard_scores=leaderboard_scores)
        self.view.clear_round_info()
      
    def handle_round_success(self): 
        self.api.end_session()
        self.view.round_success() 
        time.sleep(1)
        self.model.next_round()
        
    def handle_round_retry(self):
        self.api.end_session()
        self.view.failed_to_select()
        time.sleep(1)
        self.model.restart_round()
        
    def handle_round_failed(self):
        self.api.end_session()
        self.view.round_failed()
        time.sleep(1)
        self.model.next_round()