# imports
from api.api_data import end_session_data, getChannelData, getConfigureData, getBCIConfigurationData
import requests
from utils import make_url, make_header, handle_request_errors
import json
import os
from dotenv import load_dotenv
from UTIL.EnvironmentVariables import EnvironmentVariables

class API:
    
    # config variables
    URL_NOT_SET = "Environment variables BASE_URL and PORT are not set."
    def __init__(self, env_var:EnvironmentVariables):
        self.env_var:EnvironmentVariables = env_var

    # CONFIGURE TELEMETRY API
    # Configures impedance stream based on EXPERIMENT_NAME_PREFIX in .env file
    def callConfigureTelemetryAPI(self):
        print("API: configure Telemetry")
        experimentName = self.env_var.get_var(EnvironmentVariables.EXPERIMENT_PREFIX_KEY)
        request_body = getConfigureData(experimentName)
        self.makeRequest('configure', request_body)


    # END SESSION API
    # Tells Cognixion ecosystem to end impedance data stream from board.
    def callEndSessionAPI(self):
        print("API: end session")
        # Prepare the request data
        request_body = end_session_data
        self.makeRequest('end', request_body)
        

    # MEASURE_IMPEDANCE_COMMAND API
    # Tells Cognixion ecosystem to stream current (singular) impedance value from a given channel.
    # params: int channel
    # int channel: channel to request impedance value for
    def callImpedanceAPI(self,channel):
        print(f"API: check impedance for channel {channel + 1}")
        # Prepare the request data
        request_body = getChannelData(channel + 1)
        self.makeRequest('impedance', request_body)


    def callBCIConfigurationAPI(self):
        print("API: configure BCI")
        request_body = getBCIConfigurationData()
        self.makeRequest('configure', request_body)
        
        
    def makeRequest(self,endpoint, request_body) :
        # Construct the request URL
        base_url = self.env_var.get_var(EnvironmentVariables.BASE_URL_KEY)
        port = self.env_var.get_var(EnvironmentVariables.PORT_KEY)
        
        if base_url is None or port is None:
            print(API.URL_NOT_SET)
            return
        
        request_url = make_url(base_url, port, endpoint)

        headers = make_header()

        # Send API POST Request to server, handle errors if necessary.
        try:
            response = requests.post(request_url, data=json.dumps(request_body), headers=headers)
            response.raise_for_status()
            
            print(f"Response Content: {response.text}")

        except Exception as e:
            handle_request_errors(e)