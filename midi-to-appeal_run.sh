#!/bin/bash

echo "Creating virtual environment..."

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "Virtual environment created."
else
    echo "Virtual environment already exists."
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install requirements if requirements.txt exists
if [ -f "requirements.txt" ]; then
    echo "Installing requirements..."
    pip install -r requirements.txt
fi

# Run the GUI application
echo "Running gui_app.py..."
sudo venv/Scripts/python gui_app.py

# Check if the script ran successfully
if [ $? -ne 0 ]; then
    echo ""
    echo "An error occurred. Press Enter to exit."
    read
fi

# Deactivate virtual environment
deactivate