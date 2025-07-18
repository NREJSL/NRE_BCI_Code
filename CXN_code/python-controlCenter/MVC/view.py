import os.path
import tkinter as tk 
from tkinter import *
from tkinter.ttk import *
from UTIL.EnvironmentVariables import EnvironmentVariables 
from UTIL.event import Event 
from tkinter import filedialog
import json 
 
# The View class is responsible for displaying the buttons to the screen and firing events for when the user interacts with the application
class View:
    error_no_env = "No .env file found. Please restart the App."
    error_no_env_sample = "Unable to create .env file as the .env.sample is missing. \nPlease make sure that .env.sample file is present."
    
    def __init__(self, app_version:str, envVars:EnvironmentVariables, is_started:bool):
        #^events
        self.on_start_btn_pressed:Event = Event()
        self.on_stop_btn_pressed:Event = Event()
        self.on_configure_btn_pressed:Event = Event()
        self.on_configure_telemetry_btn_pressed:Event = Event()
        self.on_start_telemetry_btn_pressed:Event = Event()     
        
        self.on_close_edit_variables_btn_pressed:Event = Event()
        self.on_save_variables_btn_pressed:Event = Event()
        self.on_open_edit_variables_pressed:Event = Event()
        self.on_json_uploaded:Event = Event()
        
        
        #^Members        
        self.envVars:EnvironmentVariables = envVars
        self.app_version:str = app_version
        self.is_started:tk.BooleanVar = is_started
        #^Members - tk elements
        self._window:tk.Tk  = None
        self._btn_start:tk.Button = None
        self._btn_configure:tk.Button = None
        self._btn_configure_telemetry:tk.Button = None
        self._btn_stop:tk.Button = None
        self._btn_start_telemetry:tk.Button = None
        self._btn_upload_json:tk.Button = None
        #^ configure screen
        self._config_window:tk.Tk = None
        self._save_btn:tk.Button = None
        self.form_entries = {}
        
        self._create_window()
        
    def _create_window(self):
        self._window = tk.Tk()
        title = f"python-controlCenter v{self.app_version}"
        self._window.title(title)
        
        # Configure grid layout
        self._window.columnconfigure([0, 1], weight=1, minsize=75)
        self._window.rowconfigure([0, 1, 2, 3, 4, 5], weight=1, minsize=50)
        
        # set to true if the user has pressed Start and false if the user has pressed Stop
      

        btn_padx = 30
        btn_pady = 12
        btn_width = 15
        
        self._create_btns(btn_padx = btn_padx, btn_pady = btn_pady, btn_width = btn_width) 
    
    def _create_btns(self,btn_padx:int, btn_pady:int, btn_width:int):
        # Create buttons and entry field
        self._btn_configure_telemetry = tk.Button(
            master=self._window,
            text="Configure Telemetry",
            padx=btn_padx, 
            pady=btn_pady,
            width=btn_width,
            command=lambda: self.on_configure_telemetry_btn_pressed.trigger()
        )
        self._btn_configure = tk.Button(
            master=self._window,
            text="Config BCI Studio",
            padx=btn_padx,
            pady=btn_pady,
            width=btn_width,
            command=lambda: self.on_configure_btn_pressed.trigger()
        )
        self._btn_start = tk.Button(
            master=self._window,
            text="Start Stimuli",
            padx=btn_padx,
            pady=btn_pady,
            width=btn_width,
            command=lambda: self.on_start_btn_pressed.trigger(),
            state=tk.DISABLED 
        )
        self._btn_stop = tk.Button(
            master=self._window,
            text="End Stimuli",
            padx=btn_padx,
            pady=btn_pady,
            width=btn_width, 
            command=lambda: self.on_stop_btn_pressed.trigger(), 
            state=tk.DISABLED 
        )
        self._btn_start_telemetry = tk.Button(
            master=self._window,
            text="Free Run Telemetry",
            padx=btn_padx,
            pady=btn_pady,
            width=btn_width,
            command=lambda: self.on_start_telemetry_btn_pressed.trigger(), 
            state=tk.NORMAL
        )
        self._btn_open_config_page = tk.Button(
            master= self._window,
            text="Edit Environment Variables",
            padx=btn_padx,
            pady=btn_pady,
            width=btn_width,
            command=lambda: self.on_open_edit_variables_pressed.trigger(), 
            state=tk.NORMAL
        )
         
        self._btn_upload_json = tk.Button(
            master= self._window,
            text="Upload Stimuli Config JSON",
            padx=btn_padx,
            pady=btn_pady,
            width=btn_width,
            command= self.upload_json, 
            state=tk.NORMAL
        )
        
        # Grid layout placement
        self._btn_configure_telemetry.grid(row=0, column=0, padx=10, pady = 10)
        self._btn_start_telemetry.grid(row=1, column=0, padx=10, pady=10)
        self._btn_configure.grid(row=2, column=0, padx=10, pady=10)
        self._btn_upload_json.grid(row=2,column=1,padx=10,pady=10)
        self._btn_start.grid(row=3, column=0, padx=10, pady=10)
        self._btn_stop.grid(row=4, column=0, padx=10, pady=10)
        self._btn_open_config_page.grid(row=5,column=0, padx = 10, pady = 10)

    def upload_json(self):
        print("in upload json")
        # Open a file dialog to select a JSON file
        file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        
        # Check if a file was selected
        if file_path:
            # Read the JSON file
            with open(file_path, 'r') as file:
                try:
                    data = json.load(file)
                    # Process the JSON data here
                    print("JSON data:", data) 
                    self.on_json_uploaded.trigger(data)
                except json.JSONDecodeError:
                    print("Error: Invalid JSON file")    
    
    def start_gui(self):
        self._window.mainloop()  

    #control the active state of the buttons
    def toggle_controls(self, state:bool):
        
        if state is True:
            self._btn_start.configure(state=tk.DISABLED)
            self._btn_start_telemetry.configure(state=tk.DISABLED)
            self._btn_stop.configure(state=tk.NORMAL)
        else:
            self._btn_start.configure(state=tk.NORMAL)
            self._btn_start_telemetry.configure(state=tk.NORMAL)
            self._btn_stop.configure(state=tk.DISABLED)
    
    def toggle_start_controls(self, state:bool):
        if state is True:
            self._btn_start.configure(state=NORMAL)
            self._btn_start_telemetry.configure(state=NORMAL)
        else:
            self._btn_start.configure(state=DISABLED)
            self._btn_start_telemetry.configure(state=DISABLED)
            

    def close_app_configuration_screen(self):        
        if self._config_window is None:
            return
        self._config_window.destroy()
    
    def open_app_configuration_screen(self, skip_keys):
        
        self._config_window = tk.Toplevel(self._window)
        self._config_window.title("Configure Environment Variables")
        
        row = 0
        env_vars = self.envVars.get_all()
        self.form_entries = {}

        if len(env_vars) == 0 and not os.path.exists('.env.sample'):
            print(View.error_no_env_sample)
            label = Label(master=self._config_window,
                            text = View.error_no_env_sample,
                            padding= 20)
            label.grid(row=row,column=0)
            row += 2
        elif not os.path.exists('.env') and os.path.exists('.env.sample'):
            print(View.error_no_env)
            label = Label(master=self._config_window,
                            text = View.error_no_env,
                            padding= 20)
            label.grid(row=row,column=0)
            row += 2
        
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
        