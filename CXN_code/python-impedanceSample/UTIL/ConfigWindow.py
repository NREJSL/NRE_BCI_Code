import os.path
import tkinter as tk
from tkinter import *
from tkinter.ttk import * 
from UTIL.event import Event
from UTIL.EnvironmentVariables import EnvironmentVariables


# this is a class which will open a new window 
class ConfigWindow:
    error_no_env = "No .env file found. Please restart the App."
    error_no_env_sample = "Unable to create .env file as the .env.sample is missing. \nPlease make sure that .env.sample file is present."
    
    def __init__(self, env_var:EnvironmentVariables, root:tk.Tk):
        #^Defining Events
        self.on_close_btn_pressed:Event = Event()
        self.on_save_btn_pressed:Event = Event()
        
        self.on_close_btn_pressed.subscribe_handler(self._handle_close_btn_pressed)
        self.on_save_btn_pressed.subscribe_handler(self._handle_save_btn_pressed)
        
        #^Members
        self.env_var:EnvironmentVariables = env_var
        
        #^Defining Tk members
        self.root:tk.Tk = root
        self._config_window:tk.Toplevel
        self._close_btn:tk.Button
        self._save_btn:tk.Button
           
        
    #Open the window
    def open_env_config_window(self, skip_keys:list[str]):
        self._config_window = tk.Toplevel(self.root)
        self._config_window.title("Configure Environment Variables")
        
        self.form_entries = {}
        row = 0
        env_var_value = self.env_var.get_all().items()

        if len(env_var_value) == 0 and not os.path.exists('.env.sample'):
            print(ConfigWindow.error_no_env_sample)
            label = Label(master=self._config_window,
                            text = ConfigWindow.error_no_env_sample,
                            padding= 20)
            label.grid(row=row,column=0)
            row += 2
        elif not os.path.exists('.env') and os.path.exists('.env.sample'):
            print(ConfigWindow.error_no_env)
            label = Label(master=self._config_window,
                            text = ConfigWindow.error_no_env,
                            padding= 20)
            label.grid(row=row,column=0)
            row += 2

        for key, value in env_var_value:
            print(f"{key}: {value}")
            label = Label(master=self._config_window,
                          text = str(key),
                          padding= 20)
            field_str = tk.StringVar()
            field_str.set(value)
        
            entry = tk.Entry(
                master=self._config_window,
                textvariable=field_str,
                width=20)
            
            self.form_entries[key] = field_str
            
            if key in skip_keys:
                label.grid_forget()
                entry.grid_forget()
            else:
                label.grid(row=row,column=0)
                entry.grid(row=row,column=1)
                row+=2
                
        self._close_btn = tk.Button(
            master=self._config_window,
            text= "Close without Saving",
            command= lambda: self.on_close_btn_pressed.trigger()
        ).grid(row=row, column=0)
        
        self._save_btn = tk.Button(
            master=self._config_window,
            text="Save new .env",
            command= lambda: self.on_save_btn_pressed.trigger(self.form_entries)
        ).grid(row=row, column=1)
    
    #Close the window
    def close_env_config_window(self):
        if self._config_window is None:
            return
        self._config_window.destroy()
        
    #^ Private Event Handlers  
    def _handle_close_btn_pressed(self):
        self.close_env_config_window()
        
    def _handle_save_btn_pressed(self, entries):
        data = {}
        for key, value in entries.items():
            value_str = value.get()
            
            if key == EnvironmentVariables.BASE_URL_KEY and ":" in value_str:
                if not (value_str[0] == "[" and value_str[-1] == "]"):
                    value_str = "{}{}{}".format("[",value_str,"]")
                    
            print(f"{key},{value_str}")
            data[key] = value_str
        
        self.env_var.save_new_values(data)          
        self._handle_close_btn_pressed()