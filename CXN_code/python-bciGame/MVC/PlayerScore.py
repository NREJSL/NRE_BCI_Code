class GameResults():
    def __init__(self, total_targets:int, total_rounds:int):
        
        
        #^ Performance  
        self.selection_times:list[float] = []
        self.total_classification_attempts:int = 0
        self.successful_classifications:int = 0
        #^ game settings
        self.total_targets:int  = total_targets 
        self.total_rounds:int = total_rounds
        
    def correct_selection(self):
        self.successful_classifications += 1
        self.total_classification_attempts += 1
    
    def incorrect_selection(self):
        self.total_classification_attempts += 1
        
    def add_selection_time(self, newTime:float):
        self.selection_times.append(newTime)
    
        