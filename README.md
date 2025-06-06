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

- The synth is monophonic and legato.
  
- Notes are triggered via keyboard movement inputs:
  - W, A, S, D for basic notes.
  - Combinations like W+A, A+D, etc., expand the available notes.

- To access the second octave, hold `MOUSE2` while pressing the Appeal input: `MOUSE1`.

### Sound Traits by Class
Each class has its own unique waveform/sound style:

- Enforcer: **Pulse wave** 

- Scout: **Sawtooth wave**

- Infiltrator: **Sine wave**

Special Characters
Unlike standard classes, special characters (Ocelot, Snake, Quiet) use a drum kit rather than synth-based tones

## How does this script work

<p align="center">
  <img src="https://github.com/krovskiy/midi-to-appeal/raw/main/images/1.jpg" width="400">
</p>

<details>
<summary><strong>Settings Overview</strong></summary>

<br/>

<h4>Channel (int: 1–16)</h4>
<p>Specifies the MIDI channel to send data on. Standard MIDI supports 16 channels (1–16). Routes the correct notes from the desired instrument or track.</p>

<h4>BPM (int: 80–180)</h4>
<p>Controls the tempo of the playback. Valid range is between 80–180. Slower is sometimes better because of the legato function.</p>

<h4>Chord (ComboBox – str)</h4>
<p>Dropdown selection containing various musical chords. Selected chords are transposed and mapped to the 'Appeal' system.</p>

<h4>Mode (ComboBox – str)</h4>
<p>Defines the sound type. Default characters use synth; special ones use drumkits.</p>

<h4>Start Key (QLineEdit – str)</h4>
<p>The key that initiates the playback. Pressing the defined start key will begin the performance or sequence.</p>

<h4>Stop Key (QLineEdit – str)</h4>
<p>The key that stops the playback. Pressing the defined stop key will halt the performance.</p>

<h4>Root Note (ComboBox – str)</h4>
<p>Adjusts the root of the selected chord either down ('Lower') or up ('Higher') by an octave at the beginning.</p>

<h4>Status (str: 'Idle' / 'Completed' / 'Playing' / 'Stopped')</h4>
<p>Indicates the current state of the system:</p>
<ul>
  <li><strong>⬜ Idle</strong>: Awaiting input.</li>
  <li><strong>🟩 Playing</strong>: Currently active and performing.</li>
  <li><strong>🟥 Stopped</strong>: Manually halted.</li>
  <li><strong>🟦 Completed</strong>: Finished a full playback process.</li>
</ul>

<h4>Open File (QDialog – str)</h4>
<p>Opens and loads a MIDI file into the program.</p>

</details>


## TO-DO List

- [ ] Use both octaves instead of just one  
- [x] Add a config file  
- [ ] Allow color customization  
- [ ] Add `drumkit` mode for special characters  
- [x] Switch to PySide6  
- [ ] Optimize the code 
- [ ] Add note length (e.g. 0.2 - 0.8 ms) 

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
   nuitka --standalone --enable-plugin=pyside6 --include-data-dir=materials=materials --include-data-dir=fonts=fonts --include-data-file=config.ini=config.ini --output-dir=dist --output-filename=midi-to-appeal --windows-icon-from-ico=./materials/icon.ico --windows-console-mode=disable gui_app.py
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
    midi-to-appeal_run.bat
    ```
    
    **Linux:**
    ```bash
    ./midi-to-appeal.sh
    ```
3. **(Windows) Using the EXE file from Releases - not recommended**
   - Download the latest `.exe` from [Releases](https://github.com/krovskiy/midi-to-appeal/releases).
   - Place the `materials`, `fonts`, and `config.ini` in the same folder as the `.exe` if not bundled.
   - Double-click the `.exe` to run the application.
     
   **Note:** Some antivirus software may flag the executable. If you don't trust it, just use the other methods above. 🚩
<p align="center">
  <img src="https://github.com/krovskiy/midi-to-appeal/blob/main/materials/stopped.gif" width="100" alt="logo" align=center>
</p>
