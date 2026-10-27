@echo off
setlocal
cd /d "%~dp0"

where py >nul 2>nul
if errorlevel 1 (
    echo Python Launcher was not found. Install Python 3 and try again.
    exit /b 1
)

if not exist ".venv\Scripts\python.exe" (
    py -3 -m venv .venv
    if errorlevel 1 (
        echo Could not create the local Python environment.
        exit /b 1
    )

    ".venv\Scripts\python.exe" -m pip install --disable-pip-version-check -r requirements.txt
    if errorlevel 1 (
        echo Could not install project dependencies.
        exit /b 1
    )
)

".venv\Scripts\python.exe" server.py
if errorlevel 1 (
    echo The application stopped with an error.
    exit /b 1
)
