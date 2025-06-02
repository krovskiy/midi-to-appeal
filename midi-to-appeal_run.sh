#!/bin/bash

echo "Creating virtual environment..."

if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "Virtual environment created."
else
    echo "Virtual environment already exists."
fi

echo "Activating virtual environment..."
source venv/bin/activate

if [ -f "requirements.txt" ]; then
    echo "Installing requirements..."
    pip install -r requirements.txt
fi

echo "Running gui_app.py..."
sudo venv/Scripts/python gui_app.py

if [ $? -ne 0 ]; then
    echo ""
    echo "An error occurred. Press Enter to exit."
    read
fi

deactivate