@echo off

REM Save the batch file's location (assuming it's in the project directory)
set "ORIG_DIR=%~dp0"

REM Change directory to the virtual environment's Scripts folder
cd "%ORIG_DIR%\CXN_env\Scripts"

REM Activate the virtual environment
powershell -ExecutionPolicy Bypass -Command "& '.\Activate.ps1'"

REM Go two levels up from the batch file's original directory, then into python-controlCenter
cd "%ORIG_DIR%\python-controlCenter"

REM Run the Python script
python app.py

REM Pause to display any output or error messages
pause
