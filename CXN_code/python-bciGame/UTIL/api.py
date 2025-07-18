import time 
import sys
import requests
import csv
from threading import Thread
import numpy as np
from pylsl import StreamInlet, resolve_stream, StreamOutlet, StreamInfo
import signal
from dotenv import load_dotenv 
from UTIL.event import Event
from UTIL.api_data import APIData
import json
from UTIL.EnvironmentVariables import EnvironmentVariables 

class API():
    
    #Constants
    CONFIGURE_ENDPOINT:str = 'configure' 
    START_SESSION_ENDPOINT:str = 'start'
    END_SESSION_ENDPOINT:str = 'end'
    STIM_SHAPE:str = "CIRCLE"
    
    
    
        
    def __init__(self, env_var:EnvironmentVariables):  
        #^ Events
        self.on_api_error:Event = Event()
        
        #^ Members 
        self.env_var:EnvironmentVariables = env_var
        self.api_data:APIData  = APIData() 
        
    #^ Axon R Requests
    def configure_telemetry(self):
        json_body = APIData.get_configure_telemetry_data(self.env_var.get_var(EnvironmentVariables.PREFIX_KEY))
        print(f"API: configuring telemetry")
        request_url = self.make_url(endpoint=self.CONFIGURE_ENDPOINT)
        headers = API.make_request_header()
        self.post_request(request_url,headers,json_body,api_method="configure_telemetry")
        
    def configure_bci(self):
        print("API: configuring bci")
        request_url = self.make_url(endpoint=self.CONFIGURE_ENDPOINT)
        headers = API.make_request_header()
        json_body = APIData.bci_config_data
        self.post_request(request_url,headers,json_body,api_method="configure_bci")  
        
    def configure_stimuli(self,layout:int):
        print("API: configuring stimuli layout:" + str(layout))
        request_url = self.make_url(endpoint=self.CONFIGURE_ENDPOINT)
        headers = API.make_request_header() 
        config_json = self.get_stimuli_json(layout_num = layout)
        
        self.post_request(request_url,headers,config_json, api_method="configure_stimuli")
    
    def start_session(self):
        print("API: starting session")
        request_url = self.make_url(endpoint=self.START_SESSION_ENDPOINT)
        headers = API.make_request_header()
        json_data = APIData.start_session_data
        
        self.post_request(request_url,headers,json_data,api_method="start_session")
    
    def end_session(self):
        print("API: End session")
        request_url = self.make_url(endpoint=self.END_SESSION_ENDPOINT)
        self.post_request(request_url, API.make_request_header(), APIData.end_session_data, api_method="end_session")
   
   
    #^ Helpers
    def get_stimuli_json(self, layout_num:int):
        if(layout_num == 8):
            return APIData.get_eight_stimuli_layout(self.STIM_SHAPE)
        if(layout_num == 12):
            return APIData.get_twelve_stimuli_layout(self.STIM_SHAPE)
        
        return APIData.get_four_stimuli_layout(self.STIM_SHAPE)
    
    def make_url(self, endpoint):
        return f'http://{self.env_var.get_var(EnvironmentVariables.BASE_URL_KEY)}:{self.env_var.get_var(EnvironmentVariables.PORT_KEY)}/v1/{endpoint}'
    
    def make_request_header():
        return {
            'Content-Type': 'application/json'
        }
    
    def handle_request_errors(self,api_method,e):
        error_msg = ""
        
        if isinstance(e, requests.exceptions.RequestException):    
            error_msg = f"Request Error: {e}"
        elif isinstance(e, requests.exceptions.HTTPError):
            error_msg = f"HTTP Error: {e}"
        elif isinstance(e, requests.exceptions.Timeout):
            error_msg = f"Request timed out: {e}"
        else:
            error_msg = f"An unexpected error occurred: {e}"
            
        print("\n" + error_msg)
        self.on_api_error.trigger(error_msg, api_method)
    
    def _get_test_flag(self)->bool:
       return str(self.env_var.get_var(EnvironmentVariables.TEST_FLAG_KEY)) == "1" 
    
           
    def post_request(self, request_url, headers, json_data, api_method:str = ""):
    
        if self._get_test_flag():
           print("Testing UI only. Won't send Post Request \n") 
           return
        
        try: 
            print(f"Time: {self.__get_time__()} Posting request to {request_url} with data: {json_data} \n")
            response = requests.post(
                request_url,
                data= json.dumps(json_data),
                headers=headers,
                timeout=10
            )
            response.raise_for_status()
            print(f"Time: {self.__get_time__()} Response Status Code: {response.status_code}")
            print(f"Time: {self.__get_time__()} Response Content: {response.text} \n")
            
        except Exception as e:
           self.handle_request_errors(api_method=api_method, e=e)
        return 
            
        
    def __get_time__(self):
        t = str(time.time()).split(".")
        return t[0][-4:] + "." + t[1][0:2]
