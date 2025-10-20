@echo off
REM FlashRecord - Fast, Simple, Easy Screen Recording
REM Start script for FlashRecord CLI

cd /d "%~dp0"

echo.
echo ========================================
echo FlashRecord - Starting...
echo ========================================
echo.

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python not found
    echo Please install Python first
    pause
    exit /b 1
)

REM Check terminalizer
terminalizer --version >nul 2>&1
if errorlevel 1 (
    echo Warning: terminalizer not found
    echo Install: npm install -g terminalizer
)

REM Start FlashRecord CLI
python -m flashrecord.cli

pause
