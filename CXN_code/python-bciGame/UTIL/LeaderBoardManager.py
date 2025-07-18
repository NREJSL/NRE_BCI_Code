
import json
from MVC.resultsModel import GameStats
from UTIL.EnvironmentVariables import EnvironmentVariables
class LeaderBoardManager():
     
    def __init__(self, env_var:EnvironmentVariables):
        self.env_var = env_var 
        self.leaderboard = self.load_leaderboard()
    
    def load_leaderboard(self):
        try:
            with open (self.env_var.get_var(EnvironmentVariables.LEADER_BOARD_PATH_KEY), 'r') as file:
                data = json.load(file)
                return [GameStats.from_dict(entry) for entry in data]
        except FileNotFoundError as e:
            print("An error occurred:", e)
            return [] 
        except json.decoder.JSONDecodeError as e:
            print("An error occurred:", e)
            return []
        
    def save_leaderboard(self):
        data = [entry.to_dict() for entry in self.leaderboard]
        with open(self.env_var.get_var(EnvironmentVariables.LEADER_BOARD_PATH_KEY), 'w') as file:
            json.dump(data, file)
        
    def add_score(self, stats:GameStats):
        self.leaderboard.append(stats)
        self.save_leaderboard()
    
    def get_leaderboard(self, count:int = 10):
        return sorted(self.leaderboard, key=lambda x: x.itr, reverse=True)[:count]
    
    
    