@echo off
echo Creating virtual environment...

REM Create virtual environment if it doesn't exist
if not exist "venv" (
    python -m venv venv
    echo Virtual environment created.
) else (
    echo Virtual environment already exists.
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install requirements if requirements.txt exists
if exist "requirements.txt" (
    echo Installing requirements...
    pip install -r requirements.txt
)

REM Run the GUI application
echo Running gui_app.py...
python gui_app.py

REM Keep the window open if there's an error
if errorlevel 1 (
    echo.
    echo An error occurred. Press any key to exit.
    pause >nul
)

REM Deactivate virtual environment
deactivate