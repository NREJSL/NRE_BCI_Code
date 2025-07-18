
class GameStats():

    def __init__(self, name:str = "", min:float = 0, max:float = 0, avg:float = 0, correct:float = 0,itr:float = 0, warning:str = ""):
        self.name:str = name
        self.min_selection_time:float = min
        self.avg_selection_time:float = avg
        self.max_selection_time:float = max
        self.percent_correct:float = correct
        self.itr:float = itr
        self.warning:str = warning
                
    def set_name(self, name):
        self.name = name
        
    def to_dict(self):
        return {
                "name":self.name, 
                "min_selection_time":self.min_selection_time,
                "max_selection_time":self.max_selection_time,
                "avg_selection_time":self.avg_selection_time,
                "percent_correct":self.percent_correct,
                "itr":self.itr,
                "warning":self.warning
                }
        
    def to_string(self, includeName:bool = False):
        """
        to_string returns the GameStats data as a string. 
        includeName = True, will print the name field on the GameStats object.
        includeName = False, will not include the name field on the GameStats object. 
        
        returns -> String with all values of the object.
        """
        if includeName is True:
            return f"name:{self.name}, min_selection_time:{self.min_selection_time}, max_selection_time:{self.max_selection_time}, avg_selection_time:{self.avg_selection_time}, percent_correct:{self.percent_correct}, itr:{self.itr}, notes:{self.warning}"
        else:
            return f"min_selection_time:{self.min_selection_time}, max_selection_time:{self.max_selection_time}, avg_selection_time:{self.avg_selection_time}, percent_correct:{self.percent_correct}, itr:{self.itr}, notes:{self.warning}"
        
        
    @classmethod
    def from_dict(cls, data):
        return cls(
            name=data["name"],
            min=data["min_selection_time"],
            max=data["max_selection_time"],
            avg=data["avg_selection_time"],
            correct=data["percent_correct"],
            itr=data["itr"],
            warning=data["warning"])

        