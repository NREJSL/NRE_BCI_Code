from UTIL.event import Event

# This is the logical model of the app.
# it is just a boolean that has an event on changed. 
class AppModel:    
    def __init__(self):
        #^ Members
        self.is_started:bool = False
        self.stimuli_is_configure: bool = False
        #^ events
        self.on_is_started_toggled:Event = Event()
        self.on_stimuli_configured:Event = Event()
        
        
    def streaming_started(self):
        self.is_started = True
        self.on_is_started_toggled.trigger(self.is_started)
    
    def streaming_stopped(self):
        self.is_started = False
        self.on_is_started_toggled.trigger(self.is_started)
        
    def stimuli_configured(self):
        self.stimuli_is_configure = True
        self.on_stimuli_configured.trigger(self.stimuli_is_configure)