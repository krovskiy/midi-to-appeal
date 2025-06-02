@echo off
echo Creating virtual environment...

if not exist "venv" (
    python -m venv venv
    echo Virtual environment created.
) else (
    echo Virtual environment already exists.
)

echo Activating virtual environment...
call venv\Scripts\activate.bat

if exist "requirements.txt" (
    echo Installing requirements...
    pip install -r requirements.txt
)

echo Running gui_app.py...
python gui_app.py

if errorlevel 1 (
    echo.
    echo An error occurred. Press any key to exit.
    pause >nul
)

deactivate