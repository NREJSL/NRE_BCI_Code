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
from tkinter import *
from tkinter.ttk import *
from UTIL.event import Event
from UTIL.EntryWithPrompt import EntryWithPrompt
from MVC.resultsModel import GameStats 
from MVC.PlayerScore import GameResults
from UTIL.EnvironmentVariables import EnvironmentVariables as EnvVar
import subprocess



class View():
        
    #^Constants
    WINDOW_SIZE:str = "1575x950"
    LEADER_BOARD_SIZE:str = "1000x400"
    SUCCESS_CLIP:str = 'success'
    FAIL_CLIP:str = 'fail'
    ROUND_FAIL_CLIP:str = 'roundFail'
    
    def __init__(self, app_version:str, env_var:EnvVar):
        
        #^ events
        self.on_start_btn_pressed:Event = Event()
        self.on_end_btn_pressed:Event = Event()
        self.on_leader_board_btn_pressed:Event = Event()
        self.on_exit_btn_pressed:Event = Event()
        self.on_window_close:Event = Event() 
        
        self.on_enter_name_btn_pressed:Event = Event()
        
        self.on_open_config_btn_pressed:Event = Event()
        self.on_close_edit_variables_btn_pressed:Event = Event()
        self.on_save_variables_btn_pressed:Event = Event()
        self.on_configure_game_btn_pressed:Event = Event()
        #! testing events
        self.on_test_btn_pressed:Event = Event()
        
        #^ TK Members
        self.root:tk.Tk = None
        self.leader_board_window:Toplevel = None
        
        self.canvas:tk.Canvas = None
        self.color_rect = None
        
        #^ TK Buttons
        self.start_btn:tk.Button =None
        self.end_btn:tk.Button = None
        self.leader_board_btn:tk.Button = None
        self.exit_btn:tk.Button = None
        self.open_config_btn:tk.Button = None
        self.configure_game_btn:tk.Button = None
    
        self.test_1_btn:tk.Button = None
        self.test_2_btn:tk.Button = None
        self.test_3_btn:tk.Button = None
        self.test_4_btn:tk.Button = None
        
        #^ Tk Leaderboard pages
        self.enter_name_btn:tk.Button = None
        self.name_input:tk.StringVar = None
        
        #^ TK Label String Variables
        self.round_text:tk.StringVar = None
        self.chances_text:tk.StringVar = None
        self.stim_target_text:tk.StringVar = None
        
        self.round_label:tk.Label = None
        self.chances_label:tk.Label = None
        self.target_label:tk.Label = None
        
          
        #^ members 
        self.env_var:EnvVar  = env_var
        self.create_window(app_version) 
        
    def _get_is_mac(self)->bool:
        """Helper method, Gets the operating system as a bool. 

        Returns:
            bool: True if EnvVar.OP_SYSTEM_KEY .env value is "mac" (case insensitive)
        """
        return str(self.env_var.get_var(EnvVar.OP_SYSTEM_KEY)).lower() == "Mac".lower() 
    
    def create_window(self, app_version:str):
        """Creates the TK elements on the main View window. 
        
        Args:
            app_version (str): the application version # as a string. Used in the title       
        """
        #^ root
        self.root = Tk()
        self.root.title(f"python-bciGame v{app_version}")
        self.root.geometry(View.WINDOW_SIZE)
        self.root.protocol("WM_DELETE_WINDOW",self.window_close)
        
        
        #^ buttons
        self.start_btn = tk.Button(
            self.root,
            text="Start Game!",
            command=self.start_btn_pressed)
        
        self.end_btn = tk.Button(
            self.root,
            text="End!",
            command=self.end_early_btn_pressed)
        
        self.leader_board_btn = tk.Button(
            self.root,
            text="Leader Board!",
            command=self.leader_board_btn_pressed)
        
        self.exit_btn = tk.Button(
            self.root,
            text="Exit App!",
            command=self.exit_btn_pressed)
        
        self.open_config_btn = tk.Button(
            self.root, 
            text="Edit .env Variables!",
            command= lambda: self.on_open_config_btn_pressed.trigger())
        
        self.configure_game_btn = tk.Button(
            self.root,
            text="Configure Game",
            command= lambda: self.on_configure_game_btn_pressed.trigger()
        )
        
        # main game buttons
        self.leader_board_btn.grid(row=3)
        self.start_btn.grid(row=1)
        self.end_btn.grid(row=2)
        # other buttons
        self.configure_game_btn.grid(row=4)
        self.open_config_btn.grid(row = 5)
        self.exit_btn.grid(row =6)
         
        self.toggle_main_buttons(False, "View.create_window")
        
        #! Testing buttons
        if(False):
            self.make_fake_btns()
       
        
        
    

        
        #^ Labels
        self.round_text = tk.StringVar(
            master=self.root,
            value="")
        
        self.chances_text = tk.StringVar(
            master=self.root,
            value="")
        
        self.stim_target_text = tk.StringVar(
            master=self.root,
            value="")
        
        self.update_canvas()
        
    def start_gui(self):
        self.root.mainloop()
        
    def close(self):
        if self._get_is_mac():
            os.system("clear")
        else:
            os.system("cls")
            
        self.root.destroy()
    
    def close_leaderboard(self):
        if self.leader_board_window is None:
            return
        self.leader_board_window.destroy()
    
    #^ Region: Button Event Methods 
    def start_btn_pressed(self): 
        self.on_start_btn_pressed.trigger()
    
    def end_early_btn_pressed(self):
        self.on_end_btn_pressed.trigger()
        
    def leader_board_btn_pressed(self):
        self.on_leader_board_btn_pressed.trigger()
        
    def exit_btn_pressed(self):
        self.on_exit_btn_pressed.trigger()

    def enter_btn_pressed(self): 
        self.on_enter_name_btn_pressed.trigger(self.name_input.get())
 
    #^ Opening the Other pages
    def open_leader_board_page(self,  game_stats:GameStats = None,   leaderboard_scores:list[GameStats] =None):

        # Toplevel object will be treated as a new window
        self.leader_board_window = Toplevel(self.root)
        self.leader_board_window.title("Leader Board")
        self.leader_board_window.geometry(View.LEADER_BOARD_SIZE)
     
        if game_stats is None and leaderboard_scores is None: 
            Label(master= self.leader_board_window, text="Nothing to see here").pack()
            return 
            
            
            
        #! Adding A new Entry After the game that just finished
        if game_stats is not None:
            
            print("Game Completed")
            print("Player Stats: \n" + game_stats.to_string(False))
            
            title_row = 1
            #titles
            Label(self.leader_board_window, text= "Game Complete!").grid(row=0, column=3)
            Label(self.leader_board_window, text=str("ITR (bits/min)"),padding=20 ).grid(row=title_row, column = 1)
            Label(self.leader_board_window, text=str("% Correct"),padding=20 ).grid(row=title_row, column = 2)
            Label(self.leader_board_window, text=str("fastest selection (sec)"),padding=20 ).grid(row=title_row, column = 3)
            Label(self.leader_board_window, text=str("slowest selection (sec)"),padding=20 ).grid(row=title_row, column = 4)
            Label(self.leader_board_window, text=str("avg selection time (sec)"),padding=20 ).grid(row=title_row, column = 5)
            Label(self.leader_board_window, text=str("Notes"), padding = 20).grid(row=title_row, column = 6)
        
            Label(self.leader_board_window, text= "Game Results:").grid(row=title_row, column=0)   
            Label(self.leader_board_window, text=str("{:.2f}".format(game_stats.itr))).grid(row=title_row + 1, column = 1)
            Label(self.leader_board_window, text=str("{:.2f}".format(game_stats.percent_correct))).grid(row=title_row + 1, column = 2)
            Label(self.leader_board_window, text=str("{:.2f}".format(game_stats.min_selection_time))).grid(row=title_row + 1, column = 3)
            Label(self.leader_board_window, text=str("{:.2f}".format(game_stats.max_selection_time))).grid(row=title_row + 1, column = 4)
            Label(self.leader_board_window, text=str("{:.2f}".format(game_stats.avg_selection_time))).grid(row=title_row + 1, column = 5)
            Label(self.leader_board_window, text=str(game_stats.warning)).grid(row=title_row + 1, column = 6)
                        
            #input
            self.name_input = tk.StringVar()
            entry = EntryWithPrompt(
                master= self.leader_board_window,
                prompt="Enter Your Name...",
                textvariable=self.name_input,
                width=20)
            entry.grid(row=title_row + 2, column = 0)    
            self.enter_name_btn = tk.Button(
                self.leader_board_window, 
                command= self.enter_btn_pressed,
                text="Enter").grid(row=title_row +2, column=1)
            
        #! Viewing existing entries
        if leaderboard_scores is not None: 
            start_row = 7
            Label(self.leader_board_window, text="Players " , padding=20).grid(row=start_row, column = 1)
            Label(self.leader_board_window, text=str("ITR (bits/min)"),padding=20 ).grid(row=start_row, column = 2)
            Label(self.leader_board_window, text=str("% Correct"),padding=20 ).grid(row=start_row, column = 3)
            Label(self.leader_board_window, text=str("fastest selection (sec)"),padding=20 ).grid(row=start_row, column = 4)
            Label(self.leader_board_window, text=str("slowest selection (sec)"),padding=20 ).grid(row=start_row, column = 5)
            Label(self.leader_board_window, text=str("avg selection time (sec)"),padding=20 ).grid(row=start_row, column = 6)
            Label(self.leader_board_window, text=str("Notes"),padding=20 ).grid(row=start_row, column = 7)
           
            i = 0
            for score in leaderboard_scores:
                i += 1
                Label(self.leader_board_window, text=str(i) ).grid(row=start_row + i, column = 0)
                Label(self.leader_board_window, text=score.name ).grid(row=start_row + i, column = 1)
                Label(self.leader_board_window, text=str("{:.2f}".format(score.itr))).grid(row=start_row + i, column = 2)
                Label(self.leader_board_window, text=str("{:.2f}".format(score.percent_correct))).grid(row=start_row + i, column = 3)
                Label(self.leader_board_window, text=str("{:.2f}".format(score.min_selection_time))).grid(row=start_row + i, column = 4)
                Label(self.leader_board_window, text=str("{:.2f}".format(score.max_selection_time))).grid(row=start_row + i, column = 5)
                Label(self.leader_board_window, text=str("{:.2f}".format(score.avg_selection_time))).grid(row=start_row + i, column = 6)
                Label(self.leader_board_window, text=score.warning).grid(row=start_row + i, column = 7)
        
    def open_app_configuration_screen(self, skip_keys):
        
        self._config_window = tk.Toplevel(self.root)
        self._config_window.title("Configure Environment Variables")
        
        env_vars = self.env_var.get_all()
        self.form_entries = {}
        
        row = 0
        for key, value in env_vars.items():
            print(f"{key}: {value}")
            label = Label(self._config_window,
                  text=str(key), 
                  padding = 20)
            
            field_str = tk.StringVar()
            field_str.set(value)
            entry = tk.Entry(
                master= self._config_window,
                textvariable=field_str,
                width=20
            )
            
            self.form_entries[key] = field_str
            
            if key in skip_keys:
                label.grid_forget()
                entry.grid_forget()
            else:
                label.grid(row=row, column = 0)
                entry.grid(row= row, column = 1)    
                row += 2
            
            
        
        self.close_config_btn = tk.Button(
            master= self._config_window,
            text="Close without Saving",
            command= lambda: self.on_close_edit_variables_btn_pressed.trigger()
        ).grid(row=row, column = 0)
        
        self.save_config_btn_pressed = tk.Button(
            master= self._config_window,
            text="Save new .env",
            command= lambda: self.on_save_variables_btn_pressed.trigger(self.form_entries)
        ).grid(row=row,column=1)
    
    def close_config_screen(self):
        if self._config_window is None:
            return
        self._config_window.destroy()
                
    def window_close(self):
        self.on_window_close.trigger(root=self.root)
    
    def make_fake_btns(self):
        self.test_1_btn = tk.Button(
            master=self.root,
            text="fake 1",
            command= lambda: self.on_test_btn_pressed.trigger(1)).grid(column= 4, row=5)
        self.test_2_btn = tk.Button(
            master=self.root,
            text="fake 2",
            command= lambda: self.on_test_btn_pressed.trigger(2)
        ).grid(column= 5, row = 5)
        self.test_3_btn = tk.Button(
            master=self.root,
            text="fake 3",
            command= lambda: self.on_test_btn_pressed.trigger(3)
        ).grid(column= 6, row =5)
        self.test_4_btn = tk.Button(
            master=self.root,
            text="fake 4",
            command= lambda: self.on_test_btn_pressed.trigger(4)
        ).grid(column= 7, row = 5)
        
        self.test_5_btn = tk.Button(
            master=self.root,
            text="fake 5",
            command= lambda: self.on_test_btn_pressed.trigger(5)).grid(column= 4, row=6)
        self.test_6_btn = tk.Button(
            master=self.root,
            text="fake 6",
            command= lambda: self.on_test_btn_pressed.trigger(6)
        ).grid(column= 5, row = 6)
        self.test_7_btn = tk.Button(
            master=self.root,
            text="fake 7",
            command= lambda: self.on_test_btn_pressed.trigger(7)
        ).grid(column= 6, row =6)
        self.test_8_btn = tk.Button(
            master=self.root,
            text="fake 8",
            command= lambda: self.on_test_btn_pressed.trigger(8)
        ).grid(column= 7, row = 6)
        
        self.test_9_btn = tk.Button(
            master=self.root,
            text="fake 9",
            command= lambda: self.on_test_btn_pressed.trigger(9)).grid(column= 4, row=7)
        self.test_10_btn = tk.Button(
            master=self.root,
            text="fake 10",
            command= lambda: self.on_test_btn_pressed.trigger(10)
        ).grid(column= 5, row = 7)
        self.test_11_btn = tk.Button(
            master=self.root,
            text="fake 11",
            command= lambda: self.on_test_btn_pressed.trigger(11)
        ).grid(column= 6, row =7)
        self.test_12_btn = tk.Button(
            master=self.root,
            text="fake 12",
            command= lambda: self.on_test_btn_pressed.trigger(12)
        ).grid(column= 7, row = 7)
        
        btn = tk.Button(
            master= self.root,
            text= "test stim config",
            command= lambda: self.on_test_btn_pressed.trigger(-1)
        ).grid(column= 0, row = 7)
        
    
     
    def set_round_info(self, 
                       total_rounds:int, 
                       current_round:int, 
                       target_stimuli:int, 
                       chances_remaining:int):
        self.round_text.set(f"Round: {current_round}/{total_rounds}")
        self.chances_text.set(f"Chances Left: {chances_remaining} ")
        self.stim_target_text.set(f"{target_stimuli}")
        self._play_audio(True,target_stimuli)
        
        self.update_canvas()
        
    def clear_round_info(self):
        self.round_text.set("")
        self.chances_text.set("")
        self.stim_target_text.set("")
        self.update_canvas()
        
        
    def toggle_main_buttons(self, on:bool, s:str):
        #print(f"***** View.toggle_main_buttons {on}. Called from {s}")
        if on == True:
            self.start_btn.configure(state=tk.NORMAL) 
            self.end_btn.configure(state=tk.NORMAL)
            self.leader_board_btn.configure(state=tk.NORMAL) 
        else:
            self.start_btn.configure(state=tk.DISABLED) 
            self.end_btn.configure(state=tk.DISABLED)
            self.leader_board_btn.configure(state=tk.DISABLED) 
            
            
        
        
    #^ Selection Feedback     
    def round_success(self):
        self.update_canvas("green") 
        self._play_audio(False, View.SUCCESS_CLIP)
        
    def failed_to_select(self):
        self.update_canvas("red") 
        self._play_audio(False,View.FAIL_CLIP)
        
    def round_failed(self):
        self.update_canvas("red") 
        self._play_audio(False,View.ROUND_FAIL_CLIP)
       
    def toggle_open_config(self, on:bool):
        self.open_config_btn.config(state= tk.ACTIVE if on == True else tk.DISABLED)
    
    #^ Region: Audio Helpers
    def _play_mp3(self, name):
        if self._get_is_mac() :         
            os.system("mpg123 -q "+ "audio/"+str(name)+".mp3" )
        else:
            file_path = f"audio/{name}.mp3"
            # subprocess.call(['powershell', '-c', f'(New-Object Media.SoundPlayer "{file_path}").PlaySync();'])
            
    def _play_wav(self, name):
        if self._get_is_mac():
             os.system("afplay "+ "audio/"+str(name)+".wav")
        else:
            file_path= f"audio/{str(name)}.wav"
            # command = f'powershell -c "(New-Object Media.SoundPlayer \'{file_path}\').PlaySync();"'
            # subprocess.call(command, shell=True)
    
    def _play_audio(self, is_mp3:bool, name:str):
        
        if int(self.env_var.get_var(EnvVar.PLAY_AUDIO_KEY)) == 0:
            return 
        
        action = None
        if is_mp3 :
            action = lambda: self._play_mp3(name)
        else:
            action = lambda: self._play_wav(name)
       
        Thread(target=action).start()
    
    #^Region: Drawing
    def update_canvas(self,color:str="lightblue"): 
        
        if(self.canvas is not None):
            self.canvas.destroy()
        
        self.canvas = tk.Canvas(self.root, width=1400, height=800, bg="white")
        self.canvas.grid(row=8,column=8)
        
        self._draw_target_text(self.stim_target_text.get(),color)
        self._draw_round_text(self.round_text.get())
        self._draw_chances_text(self.chances_text.get())
        self.root.update()
    
    def _draw_target_text(self,text, color:str = "lightblue"):
        # Draw the shape
        self.color_rect =  self.canvas.create_rectangle(450, 0, 1500, 1000, fill=color)
        # Calculate the center of the shape
        center_x = 925
        center_y = 400
        # Put the text in the middle of the shape
        self.canvas.create_text(center_x, center_y, text=text, fill="black", font=("ArialBold", 1000))
        
    
    def _draw_round_text(self,text):
        self.canvas.create_rectangle(50, 50, 390, 200, fill="black")
        self.canvas.create_rectangle(55, 55, 385, 195, fill="lightgrey")
        self.canvas.create_text(200,125, text=text, fill="black",font=("ArialBold", 40))
        
        
    def _draw_chances_text(self,text):
        self.canvas.create_rectangle(50, 550, 390, 700, fill="black")
        self.canvas.create_rectangle(55, 555, 385, 695, fill="lightgrey")
        self.canvas.create_text(200,625, text=text, fill="black",font=("ArialBold", 40))
        
  
  


     