import shutil
import os.path
from threading import Event as ThreadEvent
from dotenv import load_dotenv
from UTIL.EnvironmentVariables import EnvironmentVariables
from MVC.view import View
from MVC.controller import Controller
from MVC.model import AppModel
from UTIL.api import API
from UTIL.streamListener import StreamListener

# App.py constructs the different classes and starts the controller object
APP_VERSION = "2.2.4"

error_no_env = "No .env file found. Creating .env using .env.sample file."
error_no_env_sample = "Unable to create .env file as the .env.sample is missing. \nPlease make sure that .env.sample file is present."
 
def main():
    
    env_vars = EnvironmentVariables()

    if not os.path.exists('.env') and os.path.exists('.env.sample'):
        print(error_no_env)
        shutil.copyfile('.env.sample','.env')
        env_vars = EnvironmentVariables()
    elif not os.path.exists('.env') and not os.path.exists('.env.sample'):
        print(error_no_env_sample)
    model = AppModel()
    view = View(app_version=APP_VERSION,
                envVars=env_vars,
                is_started=model.is_started
                ) 
    controller = Controller(
        view=view,
        model = model,
        env_vars=env_vars,
        api=API(env_var=env_vars),
        streamListener=StreamListener(
            stop_event= ThreadEvent(),
            env_vars=env_vars)
        )
    controller.start_app()
 
if __name__ == "__main__":
    load_dotenv()
    main()
    
