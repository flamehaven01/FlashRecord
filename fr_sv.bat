@echo off
chcp 65001 >nul
set DURATION=%1
set FPS=%2

if "%DURATION%"=="" set DURATION=5
if "%FPS%"=="" set FPS=10

py "%~dp0flashrecord_cli_wrapper.py" @sv %DURATION% %FPS%
