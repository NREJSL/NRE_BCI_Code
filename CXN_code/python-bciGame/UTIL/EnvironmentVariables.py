import os
import os.path
import shutil
from dotenv import load_dotenv
from dotenv import dotenv_values


# EnvironmentVariables is a wrapper for the os.getenv() functionality.
# it enables getting/setting a variable in memory, retrieving all env vars, and saving new variables to file
class EnvironmentVariables:
    
    BASE_URL_KEY:str = 'BASE_URL'
    PORT_KEY:str = 'PORT' 
    DIRECTORY_PATH_KEY:str = 'DIRECTORY_PATH'
    
    OP_SYSTEM_KEY:str = 'OP_SYSTEM'
    CHANCES_KEY:str = 'CHANCES'
    ROUNDS_KEY:str = 'ROUNDS'
    LAYOUT_KEY:str = 'LAYOUT'   
    PREFIX_KEY:str = 'EXPERIMENT_NAME_PREFIX'
    POSTFIX_KEY:str = 'EXPERIMENT_NAME_POSTFIX'
    TEST_FLAG_KEY:str = 'TEST_FLAG'
    LEADER_BOARD_PATH_KEY:str = "LEADER_BOARD_PATH_KEY"
    PLAY_AUDIO_KEY:str="PLAY_AUDIO"
    
    
    
    def __init__(self):
        load_dotenv() 
        self.create_env()

    def create_env(self):
        self.env_vars_dict = dotenv_values('.env')
        if len(self.env_vars_dict) == 0 and os.path.exists('.env.sample'):
            print("No .env file found. Creating .env using .env.sample file. ")
            shutil.copyfile('.env.sample','.env')
            self.env_vars_dict = dotenv_values('.env')
        elif not os.path.exists('.env.sample'):
            error_no_env_sample = "Unable to create .env file as the .env.sample is missing. \nPlease make sure that .env.sample file is present."
            print(error_no_env_sample)
        
    
    def get_all(self):
        self.env_vars_dict = dotenv_values('.env')
        return self.env_vars_dict
    
    def save_new_values(self, entries):
        self._write_to_env_file(".env", entries)
        load_dotenv() 
        
    def _write_to_env_file(self, filename, data):
        with open(filename, 'w') as f:
            for key, value in data.items():
                f.write(f"{key}={value}\n")
                self.set_var(key,value)
                
        
    
    def get_var(self, key:str):
        
        value = ""
        try :
            value = os.getenv(key)
        except Exception as e:
            error_msg = e.args[0]
            print(f"Error retrieving EnvVar for {key}. {error_msg}")
            
        return value
    
    def set_var(self, key:str, value):
        if key is None or value is None: 
            print(f"key value pair has None value: {key}, {value}")
            return 
        
        os.environ[key] = value
    