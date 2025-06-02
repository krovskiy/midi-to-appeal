<p align="center">
  <img src="https://github.com/krovskiy/midi-to-appeal/blob/main/materials/si3lEuEp2Fk.png" width="140" alt="logo" align=center>
  &nbsp; &nbsp;
  <img src="https://github.com/krovskiy/midi-to-appeal/blob/main/images/logo.png" width="400" alt="logo" align=center>
</p>

# 

> “up up down down left right left right b a”

A MIDI-to-appeal converter that plays your favorite melodies in [MGO3](https://www.youtube.com/watch?v=rY1XP5YNrQI)!


## Features

- Play MIDI files through the appeal action system in MGO3
- Animated status indicators (idle, playing, completed, stopped)
- Hotkey support for start/stop playback (configurable)
- Cross-platform: Windows & Linux

## Context

In Metal Gear Online 3, every class — *Scout, Enforcer, and Infiltrator* — features an 'Appeal' system, which can be activated by holding `MOUSE3`. While primarily used to display character poses on the battlefield, the 'Appeal' system also serves as a simple musical interface.

### Musical Functionality
- The system is tuned to the B Major / G# Minor scale.

- It includes 8 notes (from B to B*), spanning across two octaves (B4–B6).
  
- Notes are triggered via keyboard movement inputs:
  - W, A, S, D for basic notes.
  - Combinations like W+A, A+D, etc., expand the available notes.

- To access the second octave, hold `MOUSE2` while pressing the Appeal input: `MOUSE1`.

### Sound Traits by Class
Each class has its own unique waveform/sound style:

- Enforcer: (waveform: [blank])

- Scout: (waveform: [blank])

- Infiltrator: (waveform: [blank])

Special Characters
Unlike standard classes, special characters (Ocelot, Snake, Quiet) use a drum kit rather than synth-based tones

## How does this script work

## TO-DO List

- [ ] Use both octaves instead of just one  
- [x] Add a config file  
- [ ] Allow color customization  
- [ ] Add `drumkit` mode for special characters  
- [x] Switch to PySide6  
- [ ] Optimize the code  

## Requirements

- [Python 3.8+](https://www.python.org/downloads/)
- [umidiparser](https://github.com/bixb922/umidiparser)
- [PySide6](https://pypi.org/project/PySide6/)
- [qdarkstyle](https://pypi.org/project/qdarkstyle/)
- [keyboard](https://pypi.org/project/keyboard/)
- [pynput (for Linux)](https://pypi.org/project/pynput/)

## Installation

1. **Clone the repository:**
   ```sh
   git clone https://github.com/krovskiy/midi-to-appeal.git
   cd midi-to-appeal
2. **Create a virtual environment:**
   ```sh
    python -m venv venv
    venv\Scripts\activate   # On Windows
    # or
    source venv/bin/activate  # On Linux/macOS
   ```
3. **Install the dependencies:**
   ```sh
   pip install -r requirements.txt
   ```
4. **(Optional) Build your application with Nuitka from source:**
   ```sh
   nuitka --standalone --enable-plugin=pyside6 --include-data-dir=materials=materials --include-data-dir=fonts=fonts --include-data-file=icon.png=icon.png --include-data-file=config.ini=config.ini --output-dir=dist - output-filename=midi-to-appeal --windows-icon-from-ico=icon.ico --windows-disable-console gui_app.py
   ```
## Usage
### There are multiple ways to run the application:
1. **Running directly from the Python file:**
   
   **Windows:**
   ```sh
   python gui_app.py
   ```
   **Linux:**
   ```sh
   sudo bin/python gui.app.py
   ```
   - this is a bit unsafe, but it works (normally, you shouldn't run this with sudo lol) 
2. **Running using the .bat file or .sh**

   **Windows:**
    ```cmd
    run_app.bat
    ```
    
    **Linux:**
    ```bash
    ./run_app.sh
    ```
3. **(Windows) Using the EXE file from Releases - not recommended**
   - Download the latest `.exe` from [Releases](https://github.com/krovskiy/midi-to-appeal/releases).
   - Place the `materials`, `fonts`, and `config.ini` in the same folder as the `.exe` if not bundled.
   - Double-click the `.exe` to run the application.
     
   **Note:** Some antivirus software may flag the executable. If you don't trust it, just use the other methods above. 🚩
<p align="center">
  <img src="https://github.com/krovskiy/midi-to-appeal/blob/main/materials/stopped.gif" width="100" alt="logo" align=center>
</p>
