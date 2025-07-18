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
import random
from UTIL.event import Event
from MVC.PlayerScore import GameResults
from MVC.GameSettings import GameSettings

class GameModel():
   
   
    def __init__(self):
        #^ Members
        self.current_round:int = 0
        self.chances_remaining:int = 5

        self.last_classified_stim:int = -1
        self.round_stimuli_target:int = -1
        
        self.game_results:GameResults = None
        self.game_settings:GameSettings = None
        self.round_start_time = 0
        
            
        #^ Events
        self.on_stimuli_target_changed:Event = Event()
        self.on_game_started:Event = Event()
        self.on_game_complete:Event = Event()
        self.on_game_ended_early:Event = Event()
        
        self.on_round_started:Event  = Event()
        self.on_round_success:Event = Event()
        self.on_round_failed:Event = Event()
        self.on_round_retry:Event = Event()
        
    
    

    #^ Region: play the game
    #* start_game begins a new game
    def start_game(self,game_settings:GameSettings): 
        self.game_settings = game_settings
        self.current_round = 0
        self.chances_remaining = self.get_chances_per_round()
        self.game_results = GameResults(self.get_game_layout(), self.get_total_rounds())
        
        self.on_game_started.trigger(
            total_rounds=self.get_total_rounds(),
            chances_per_round= self.get_chances_per_round(),
            game_layout=self.get_game_layout())
        self.next_round()
        
    
    def next_round(self):
        self.round_stimuli_target = self._generate_target_number()
        self.last_classified_stim = -1
        self.chances_remaining = self.get_chances_per_round()
        self.current_round += 1
        
        if self.current_round > self.get_total_rounds(): 
            self.on_game_complete.trigger(game_results=self.game_results)
            return
        
        #raise event
        self._start_round()
    
    def restart_round(self):
        self.last_classified_stim = -1
        self.chances_remaining -= 1
        if (self.chances_remaining == 0):
            self.on_round_failed.trigger()
            return
        
        self._start_round()
          
    def _start_round(self):
        #* Raises the on_round_started event that fires at the beginning of every round
        self.round_start_time = time.time() 
        self.on_round_started.trigger(
            total_rounds = self.get_total_rounds(),
            current_round= self.current_round,
            target= self.round_stimuli_target,
            chances_left= self.chances_remaining)
        

 
 
    #^Region: Process Input 
    def input_stimuli_id(self, stimuli_id:int):
        if self.game_settings is None:
            return
        
        # two classifications that are the same, in a row.
        print("input_stimuli_id: "+ str(stimuli_id))
        if stimuli_id == self.last_classified_stim:
            #! if they are equal, then we have selected something twice in a row 
            self._stimuli_selected(stimuli_id)
            return
     
        self.last_classified_stim = stimuli_id  
            
    def _stimuli_selected(self,stimuli_id):
        print("stimuli selected: "+ str(stimuli_id))
        self.record_time()
        if(stimuli_id == self.round_stimuli_target):
            # selected the target
            self.game_results.correct_selection()
            self.on_round_success.trigger()
            return
        
        self.game_results.incorrect_selection()
        # Failed to select the target
       
         
        self.on_round_retry.trigger()
    
    def end_game_early(self):
        self.clear_game()
        self.on_game_ended_early.trigger()
       
    def clear_game(self):
        self.game_settings = None
        self.current_round = 0 
        self.chances_remaining = 0
        self.game_results = None

    def record_time(self): 
        elapsed_time = time.time() - self.round_start_time
        if self.game_results is not None: 
            self.game_results.add_selection_time(elapsed_time)
        self.round_start_time = None
    
    #^ Region: helpers      
        
        
    
    def _generate_target_number(self) -> int:
        return random.randint(1,self.get_game_layout())
    
    #^ Get Settings Method
    def get_game_layout(self) -> int:
        if self.game_settings is None:
            return 0

        return self.game_settings.game_layout
    def get_total_rounds(self) -> int:
        if self.game_settings is None:
            return 0
        
        return self.game_settings.total_rounds
    def get_chances_per_round(self) -> int:
        if self.game_settings is None:
            return 0
        
        return self.game_settings.chances_per_round