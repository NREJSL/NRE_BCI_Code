from UTIL.EnvironmentVariables import EnvironmentVariables
class GameSettings():
    
    #^ game Settings constants
    DEFAULT_ROUNDS:int = 10
    DEFAULT_CHANCES:int = 5
    FOUR_STIM_LAYOUT:int = 4
    EIGHT_STIM_LAYOUT:int = 8
    TWELVE_STIM_LAYOUT:int = 12
    AVAILABLE_LAYOUTS:list[int] = [FOUR_STIM_LAYOUT,EIGHT_STIM_LAYOUT,TWELVE_STIM_LAYOUT]
    DEFAULT_LAYOUT:int = FOUR_STIM_LAYOUT
    
    
    def __init__(self, env_var:EnvironmentVariables ):
        
        self.env_var:EnvironmentVariables = env_var
        
        #^ GameSettings
        self.game_layout:int = 4
        self.total_rounds:int = 10
        self.chances_per_round:int = 5
        
        self.validated_settings()

       
    
    def validated_settings(self):
        rounds = int(self.env_var.get_var(EnvironmentVariables.ROUNDS_KEY))
        chances = int(self.env_var.get_var(EnvironmentVariables.CHANCES_KEY))
        layout = int(self.env_var.get_var(EnvironmentVariables.LAYOUT_KEY))
                   
        if rounds <= 0:
            rounds = self.DEFAULT_ROUNDS
            
        if chances <= 0: 
            chances = self.DEFAULT_CHANCES
            
        if layout not in GameSettings.AVAILABLE_LAYOUTS:
            layout = GameSettings.DEFAULT_LAYOUT
        
        self.total_rounds =rounds
        self.chances_per_round = chances
        self.game_layout = layout
        