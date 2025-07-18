import statistics
import math
from MVC.resultsModel import GameStats
from MVC.PlayerScore import GameResults
import unittest
class StatsSolvers():     
    
    BELOW_CHANCE_WARNING:str = "accuracy is below chance"
    
    def get_game_stats(self, results:GameResults):
        min = self.get_min_selection_time(results.selection_times)
        max = self.get_max_selection_time(results.selection_times)
        avg = self.get_average_selection_time(results.selection_times)
        correct = self.get_percent_correct(
                successes=results.successful_classifications,
                attempts=results.total_classification_attempts)
        (itr,waring) = self.calculate_itr_bci(
                num_choices=results.total_targets, 
                total_attempted_classifications=results.total_classification_attempts,
                successful_selections=results.successful_classifications,
                trial_duration_seconds=self._get_duration(results.selection_times))
         
        return GameStats(
            min= min,
            max= max,
            avg=avg,
            correct=correct,
            itr= itr,
            warning=waring)
                
    def get_min_selection_time(self,selectionTimes:list[float]) -> float: 
        if selectionTimes is None or len(selectionTimes) == 0: 
            return -1
        if not isinstance( selectionTimes,list):
            return -2 
        
        sortList = sorted(selectionTimes)
        return sortList[0]
        
    def get_max_selection_time(self,selectionTimes:list[float]) -> float:
        if selectionTimes is None or len(selectionTimes) == 0: 
            return -1
        if not isinstance( selectionTimes,list):
            return -2 
    
        sortList = sorted(selectionTimes, reverse=True)
        return sortList[0]
        
    def get_average_selection_time(self,selectionTimes:list[float]) -> float:
        if selectionTimes is None or len(selectionTimes) == 0:
            return -1
        if not isinstance(selectionTimes, list):
            return -2
        
        return statistics.fmean(selectionTimes)
    
    def _get_duration(self, selectionTimes:list[float]) -> float:
        
        if selectionTimes is None or len(selectionTimes) == 0:
            return -1
        if not isinstance(selectionTimes, list): 
            return -2
     
        return sum(selectionTimes)
 
    def get_percent_correct(self,successes:int, attempts:int) ->float:
        
        if (not isinstance(attempts,int)) and (not isinstance(successes,int)):
            return -2
        
        if attempts == 0:
            return -1
        return float( successes/attempts) * 100.0

   
    
    def calculate_itr_bci(self, num_choices:int,
                          total_attempted_classifications:int, 
                          successful_selections:int, 
                          trial_duration_seconds:float, log:bool = True) -> tuple[float,str]:
        
        itr = ""
        valTotal= total_attempted_classifications
        valTime= trial_duration_seconds
        valCorrect=successful_selections
        valAccuracy = 100 * successful_selections/total_attempted_classifications    
            
        commPerMin=valTotal/(valTime/60)
        accuracy = None
        n=num_choices # number of displayed stimuli
        if(valTotal==0 or valTime==0 or valCorrect == 0):            
            return (0.0,StatsSolvers.BELOW_CHANCE_WARNING)     
        else:
            accuracy=valAccuracy/100 #Convert back from percentage
            if(accuracy <= 0):
                itr = (math.log2(n) +  (1 - accuracy)*math.log2((1 - accuracy) / (n - 1))) * commPerMin
            if(accuracy >= 1):
                itr = (math.log2(n) + accuracy*math.log2(accuracy)) * commPerMin
            else:
                itr = (math.log2(n) + accuracy*math.log2(accuracy) + (1 - accuracy)*math.log2((1 - accuracy) / (n - 1))) * commPerMin
           
             
            
            
            itr = round(itr,2)
            if(itr is None):
                itr=0.0
            
            warning = ""
            if(valAccuracy< (1/n*100)):
                # accuracy below chance
                warning = StatsSolvers.BELOW_CHANCE_WARNING
         
            return (itr, warning)
				
				
            