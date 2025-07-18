@echo off

REM Change directory to the scrcpy folder
cd C:\Users\lijun\OneDrive\Desktop\Jun_code\scrcpy-win64-v3.0.2\scrcpy-win64-v3.0.2

REM Kill any running ADB server
adb kill-server

REM Set ADB to listen over TCP/IP on port 5555
adb tcpip 5555

REM Connect to the device at the specified IP
adb connect 10.0.0.17

REM Launch scrcpy with the specific device
scrcpy.exe -e

REM Pause to display any output or error messages
pause
