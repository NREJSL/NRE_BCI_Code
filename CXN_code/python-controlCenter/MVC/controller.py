from UTIL.EnvironmentVariables import EnvironmentVariables 
from UTIL.event import Event
from MVC.view import View
from MVC.model import AppModel
from UTIL.api import API
from UTIL.streamListener import StreamListener

#Controller is responsible for hooking together the different functional components of the LSL Sample App 
class Controller:
        
    def __init__(self, view:View, model:AppModel, env_vars: EnvironmentVariables, api:API, streamListener:StreamListener):
        #^Members
        self.view:View = view
        self.model:AppModel = model
        self.env_vars:EnvironmentVariables = env_vars
        self.api:API = api
        self.streamListener:StreamListener = streamListener
        self.uploaded_stimuli_config = None
        self._sub_to_events()
    
     
    def __del__(self):
        self._un_sub_from_events()
        
    def _sub_to_events(self):
        # Subscribe to view events
        self.view.on_start_btn_pressed.subscribe_handler(self.start_btn_pressed)
        self.view.on_stop_btn_pressed.subscribe_handler(self.stop_btn_pressed)
        self.view.on_configure_btn_pressed.subscribe_handler(self.configure_btn_pressed)
        self.view.on_configure_telemetry_btn_pressed.subscribe_handler(self.configure_telemetry_btn_pressed)
        self.view.on_start_telemetry_btn_pressed.subscribe_handler(self.start_telemetry_btn_pressed)
        
        self.view.on_open_edit_variables_pressed.subscribe_handler(self.open_edit_env_pressed)
        self.view.on_save_variables_btn_pressed.subscribe_handler(self.save_env_pressed)
        self.view.on_close_edit_variables_btn_pressed.subscribe_handler(self.close_env_pressed)
        
        self.view.on_json_uploaded.subscribe_handler(self.handle_upload)
        
        
        #subscribe to API Events
        self.api.on_start_session_success.subscribe_handler(self.start_session_accepted)
        self.api.on_end_session_success.subscribe_handler(self.end_session_accepted)
        self.api.on_start_telemetry_success.subscribe_handler(self.start_telemetry_accepted)
        self.api.on_configure_bci_success.subscribe_handler(self.configure_bci_accepted)
        self.api.on_configure_stimuli_success.subscribe_handler(self.configure_stimuli_accepted)
        self.api.on_configure_telemetry_success.subscribe_handler(self.configure_telemetry_accepted)
        
        #subscribe to Model Events
        self.model.on_is_started_toggled.subscribe_handler(self.handle_is_started_changed)
        self.model.on_stimuli_configured.subscribe_handler(self.handle_stimuli_configured)
    
    def _un_sub_from_events(self):
        self.view.on_start_btn_pressed.unsubscribe_handler(self.start_btn_pressed)
        self.view.on_stop_btn_pressed.unsubscribe_handler(self.stop_btn_pressed)
        self.view.on_configure_btn_pressed.unsubscribe_handler(self.configure_btn_pressed)
        self.view.on_configure_telemetry_btn_pressed.unsubscribe_handler(self.configure_telemetry_btn_pressed)
        self.view.on_start_telemetry_btn_pressed.unsubscribe_handler(self.start_telemetry_btn_pressed)
        
        self.view.on_open_edit_variables_pressed.unsubscribe_handler(self.open_edit_env_pressed)
        self.view.on_save_variables_btn_pressed.unsubscribe_handler(self.save_env_pressed)
        self.view.on_close_edit_variables_btn_pressed.unsubscribe_handler(self.close_env_pressed)
        
        
        #subscribe to API Events
        self.api.on_start_session_success.unsubscribe_handler(self.start_session_accepted)
        self.api.on_end_session_success.unsubscribe_handler(self.end_session_accepted)
        self.api.on_start_telemetry_success.unsubscribe_handler(self.start_telemetry_accepted)
        self.api.on_configure_bci_success.unsubscribe_handler(self.configure_bci_accepted)
        self.api.on_configure_stimuli_success.unsubscribe_handler(self.configure_stimuli_accepted)
        self.api.on_configure_telemetry_success.unsubscribe_handler(self.configure_telemetry_accepted)
        
        #subscribe to Model Events
        self.model.on_is_started_toggled.unsubscribe_handler(self.handle_is_started_changed)
        
    def start_app(self):
        self.view.start_gui()
    
    
    
    #handle button pressed events
    def start_btn_pressed(self):
        self.api.configure_bci_api()
        self.api.start_session_api()
    
    def stop_btn_pressed(self):
        self.api.end_session_api()
        
    def configure_btn_pressed(self):
        self.model.streaming_stopped()
        
        self.api.configure_api(self.uploaded_stimuli_config)
        
    
    def configure_telemetry_btn_pressed(self):
        self.api.configure_telemetry_api()
    
    def start_telemetry_btn_pressed(self):
        self.api.start_telemetry_api()
    
    def open_edit_env_pressed(self): 
        skip_keys = [EnvironmentVariables.PORT_KEY, EnvironmentVariables.DIRECTORY_PATH_KEY]
        self.view.open_app_configuration_screen(skip_keys=skip_keys)
        
    def save_env_pressed(self, entries): 
        data = {}
        for key, value in entries.items(): 
            
            v_str = value.get()
            
            #check if it is an ipv6 address
            if key == EnvironmentVariables.BASE_URL_KEY and ":" in v_str:
                if not (v_str[0] == "[" and v_str[-1] == "]"):
                    v_str = "{}{}{}".format("[",v_str,"]")
                        
                     
            print(f"{key},{v_str}")   
            
            data[key] = v_str
            
        self.env_vars.save_new_values(data)    
            
        self.close_env_pressed()
            
            
            

    def close_env_pressed(self):
        self.view.close_app_configuration_screen()
        
    
    def handle_upload(self, json_data):
        self.uploaded_stimuli_config = json_data
        
   
        
        
    
    #handle api response events 
    def start_session_accepted(self):
        self.streamListener.stop_lsl_streams()
        self.streamListener.start_lsl_streams()
        print("start session accepted")
        self.model.streaming_started()
        # update UI to reflect new state
       
       
    def start_telemetry_accepted(self):
        self.streamListener.stop_lsl_streams()
        self.streamListener.start_lsl_streams()
        print("start session accepted")
        self.model.streaming_started()
        
    def configure_bci_accepted(self):
        print("Configured BCI")
        
    def configure_telemetry_accepted(self):
        print("Configured Telemetry")
    
    def configure_stimuli_accepted(self):
        print("Configured Stimuli")
        
    
    def end_session_accepted(self):
        self.streamListener.stop_lsl_streams()
        self.model.streaming_stopped()
        
      
    
    #handle model events
    def handle_is_started_changed(self, state:bool):
        self.view.toggle_controls(state=state)
    
    def handle_stimuli_configured(self, state:bool):
        self.view.toggle_start_controls(state=state)