# Change Log

All notable changes to this project will be documented in this file. Add new entries above the most recent entry. Dates follow YY-MM-DD.

The format is based on [Keep a Changelog](http://keepachangelog.com/)
and this project adheres to [Semantic Versioning](http://semver.org/).

<!---
Major-Minor-Patch - YY-MM-DD
-->
## 1.5.3 - 2024-07-17
## Breaking Changes
## Added 
- Added License.pdf file
## Changed
## Fixed 

## 1.5.2 - 2024-07-16
## Breaking Changes
## Added
- Logs for print the API calls
## Changed
## Fixed
- Creating .env file using .env.sample when missing

## 1.5.1 - 2024-06-12
## Breaking Changes
## Added
## Changed
## Fixed
- Showing `-` instead of `LEAD OFF` on startup and whilst checking impedance

## 1.5.0 - 2024-06-07
## Breaking Changes
## Added
- Added files for classes:
- - EnvironmentVariables class
- - Event class
- - ConfigWindow
- ConfigWindow opens a new window to edit the .env variables. 
## Changed 
## Fixed
 

## 1.4.1 - 2024-05-23
## Breaking Changes
## Added
## Changed 
## Fixed
- occasionally, we would receive a very large negative number the first time the check was run in a while. Added
handling of negative numbers to display LEAD OFF.  

## 1.4.0 - 2024-04-29
## Breaking Changes
## Added
- App now displays the state of the impedance check. There is text at the top of the screen that gets updated when waiting, checking, and when the check is finished. 
## Changed 
## Fixed

## 1.3.1 - 2024-04-25
## Breaking Changes
## Added
## Changed
- updated readme.md to have commands for windows
- added note about how 3.11 doesn't work for macOS
## Fixed

## 1.3.0 - 24-04-19
### Breaking Changes
### Added
- We are starting a changelog for this project. This will start with version 1.3.0. Previous versions are not documented in this changelog.  
- added AppVersion global varaible to controller.py representing the version of the application. 
### Changed
- updated the readme.md by changing the version to python3.12 
### Fixed

