# Change Log

All notable changes to this project will be documented in this file. Add new entries above the most recent entry. Dates follow YY-MM-DD.

The format is based on [Keep a Changelog](http://keepachangelog.com/)
and this project adheres to [Semantic Versioning](http://semver.org/).

<!---
Major-Minor-Patch - YY-MM-DD
-->
## 0.5.4 - 2024-07-16
## Breaking Changes
## Added
- added LICENSE.pdf file
## Changed
## Fixed


## 0.5.3 - 2024-07-16
## Breaking Changes
## Added
## Changed
## Fixed
- Creating .env file using .env.sample when missing

## 0.5.2 - 2024-06-28
## Breaking Changes
## Added  
- prints the scores to the console when the game completes. 
## Changed 
## Fixed 


## 0.5.1 - 2024-06-21
## Breaking Changes
## Added  
## Changed
- updated sample.env to include an entry for PLAY_AUDIO=0. 
## Fixed 


## 0.5.0 - 2024-06-18
## Breaking Changes
## Added  
- More verbose logging for API calls and responses. Includes timestamps 
- correlations stream listener to print correlations data
- - Main Game buttons are disabled at launch. Must now run "Configure Game": 
- - before you are able to play the game.
- - After changing the .env file. 
- - If there is an issue with an API request  
## Changed
- adjusted stim position to be -10 < y < 10 
## Fixed 

## 0.4.1 - 2024-06-18
## Breaking Changes
## Added   
## Changed     
- adjusted default window size to fit content. 
## Fixed 
- fixed issue where leader board window wasn't displaying by no longer forcing the screen to be full screen. 

## 0.4.0 - 2024-06-06
## Breaking Changes
## Added   
- Added configuration page to the app to modify the .env variables  
- now sends bci config command at start
## Changed     
## Fixed 
- removed class variable declarations that were mistakenly thought to be instance variable declarations


## 0.3.3 - 2024-05-30
## Breaking Changes
## Added   
## Changed    
- changed the ccThreshold value in the stimuli config request bodies to 0.65
## Fixed 


## 0.3.2 - 2024-05-14
## Breaking Changes
## Added   
## Changed    
- updated the readme
- changed the sample_env.txt's placeholder Base_Url value
## Fixed 


## 0.3.1 - 2024-05-14
## Breaking Changes
## Added   
## Changed    
## Fixed
- the x button should now close the same way as the regular Exit button. This will still take a second for the thread to be cleaned up. 


## 0.3.0 - 2024-05-14
## Breaking Changes
## Added  
- added colors for success/failure feedback
- added unit  tests for the StatsSolver class
- replaced with new audio files for the numbers
## Changed   
- increased width of blue box for the 2 digit number
## Fixed
- fixed itr calculation (based on calculation: https://bci-lab.hochschule-rhein-waal.de/en/itr.html)


## 0.2.1 - 2024-05-13
## Breaking Changes
## Added  
## Changed   
## Fixed
- test flag has now been changed to use a 1 or a 0
- bound check on term_2 of itr in the StatSolver

## 0.2.0 - 2024-05-13
## Breaking Changes
## Added 
- python setup steps
## Changed 
- changed the ui to have better size
## Fixed

## 0.1.0 - 2024-05-13
## Breaking Changes
## Added 
## Changed
- displaying scores after completing the game  
## Fixed

## 0.0.0 - 2024-05-07
## Breaking Changes
## Added
- creating basic functional game
## Changed 
## Fixed


