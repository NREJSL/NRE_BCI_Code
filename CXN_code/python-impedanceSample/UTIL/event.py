class Event: 
    def __init__(self):
        self._handlers = []
        
    def subscribe_handler(self, handler):
        self._handlers.append(handler)
    
    def unsubscribe_handler(self,handler):
        if handler in self._handlers:
            self._handlers.remove(handler)
            
    def trigger(self, *args, **kwargs):
        # loop through all handlers, and fire them 
        for handler in self._handlers:
            handler(*args, ** kwargs)