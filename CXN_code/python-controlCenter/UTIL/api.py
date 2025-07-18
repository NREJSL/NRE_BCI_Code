import requests
import json
from api_data import configure_stimuli_data, start_session_data, end_session_data, get_configure_telemetry_data, start_telemetry_data, bci_config_data
from UTIL.event import Event
from UTIL.EnvironmentVariables import EnvironmentVariables

# The API class handles constructing and sending the API Requests to the Axon-R API
class API:
    
    URL_NOT_SET:str = "Environment variables BASE_URL and PORT are not set."

    def __init__(self, env_var:EnvironmentVariables): 
        #^Members
        self.env_var:EnvironmentVariables = env_var
        #^Events
        self.on_start_session_success:Event = Event()
        self.on_start_telemetry_success:Event = Event()
        self.on_end_session_success:Event = Event()
        self.on_configure_stimuli_success:Event = Event()
        self.on_configure_telemetry_success:Event = Event()
        self.on_configure_bci_success:Event = Event()
        
        
    def _send_api_request(self, base_url:str, port:str,endpoint:str,body, on_success_event:Event):
        if base_url is None or port is None:
            print(self.URL_NOT_SET)
            return
        # Construct the request URL
        request_url = self._make_url(base_url, port, endpoint=endpoint)
        print(f"Request URL: {request_url}")
        headers = self._make_header()
        
        try:
            response = requests.post(request_url, data=json.dumps(body), headers=headers, timeout=10)
            response.raise_for_status()

            print(f"Response Status Code: {response.status_code}")
            print(f"Response Content: {response.text}")
            
            on_success_event.trigger()
            
        except Exception as e:
            self._handle_request_errors(e)
        
        
        
        
    def start_session_api(self):
        print("API: start session")
        self._send_api_request(
           base_url= self.env_var.get_var(EnvironmentVariables.BASE_URL_KEY),
           port= self.env_var.get_var(EnvironmentVariables.PORT_KEY),
           endpoint="start",
           body= start_session_data,
           on_success_event= self.on_start_session_success
        )
        
    def end_session_api(self):
        print("API: end session")
        self._send_api_request(
           base_url= self.env_var.get_var(EnvironmentVariables.BASE_URL_KEY),
           port= self.env_var.get_var(EnvironmentVariables.PORT_KEY),
           endpoint="end",
           body= end_session_data,
           on_success_event= self.on_end_session_success
        )
                  
    def start_telemetry_api(self):
        print("API: start telemetry")
        self._send_api_request(
           base_url= self.env_var.get_var(EnvironmentVariables.BASE_URL_KEY),
           port= self.env_var.get_var(EnvironmentVariables.PORT_KEY),
           endpoint="startTelemetry",
           body= start_telemetry_data,
           on_success_event= self.on_start_session_success
        )
        
    def configure_api(self, json_data):
        
        if json_data is None:
            # use default
            json_data = configure_stimuli_data
        
        print("API: configure Stimuli===")
        self._send_api_request(
            base_url=self.env_var.get_var(EnvironmentVariables.BASE_URL_KEY),
            port=self.env_var.get_var(EnvironmentVariables.PORT_KEY),
            endpoint="configure",
            body= json_data,
            on_success_event= self.on_configure_stimuli_success
        )
   
    def configure_telemetry_api(self):
        print("API: configure Telemetry")
        self._send_api_request(
            base_url=self.env_var.get_var(EnvironmentVariables.BASE_URL_KEY),
            port=self.env_var.get_var(EnvironmentVariables.PORT_KEY),
            endpoint="configure",
            body= get_configure_telemetry_data(self.env_var.get_var(EnvironmentVariables.EXPERIMENT_PREFIX_KEY)),
            on_success_event= self.on_configure_telemetry_success
        )
         
    def configure_bci_api(self):
        print("API: configure BCI")
        self._send_api_request(
            base_url=self.env_var.get_var(EnvironmentVariables.BASE_URL_KEY),
            port=self.env_var.get_var(EnvironmentVariables.PORT_KEY),
            endpoint="configure",
            body=bci_config_data,
            on_success_event= self.on_configure_bci_success
        )           
           
    # private helpers       
           
            
    def _make_header(self):
        return {
            'Content-Type': 'application/json'
        }


    def _make_url(self,base_url, port, endpoint):
        return f'http://{base_url}:{port}/v1/{endpoint}'


    def _handle_request_errors(self,e):
        if isinstance(e, requests.exceptions.RequestException):
            print(f"Request Error: {e.response.text}")
        elif isinstance(e, requests.exceptions.HTTPError):
            print(f"HTTP Error: {e}")
        elif isinstance(e, requests.exceptions.Timeout):
            print(f"Request timed out: {e}")
        else:
            print(f"An unexpected error occurred: {e}")