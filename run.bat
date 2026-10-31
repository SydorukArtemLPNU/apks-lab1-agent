@echo off
rem Run hello_app from sources inside the project virtual environment.
setlocal

cd /d "%~dp0"

if not exist ".venv\Scripts\python.exe" (
    py -3 -m venv .venv 2>nul || python -m venv .venv
    if errorlevel 1 exit /b 1
)

set "PYTHONPATH=src"
".venv\Scripts\python.exe" -m hello_app %*
exit /b %errorlevel%
