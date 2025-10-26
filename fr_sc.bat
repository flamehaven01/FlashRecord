@echo off
chcp 65001 >nul
py "%~dp0flashrecord_cli_wrapper.py" @sc
