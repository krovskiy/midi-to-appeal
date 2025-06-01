import umidiparser
import threading
import time
from os import path
import pynput
from .note_mapping import note_to_hold_multiple, note_to_hold_singular

thrd = threading.Event()

keyboard = pynput.keyboard.Controller()

def get_note_key(note):
    return ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B'][note % 12]

'''

Functions to define on the how the script will take 


'''

def check_b_note_press(note, raw_note, first_b_note):
    if first_b_note is None:
        first_b_note = raw_note

    elif raw_note > first_b_note:
        for key in note_to_hold_multiple[note]:
            keyboard.press(key)

    elif raw_note < first_b_note:
        keyboard.press(note_to_hold_singular[note])

    return first_b_note

def check_b_note_release(note, raw_note, first_b_note):
    if raw_note > first_b_note and note in note_to_hold_multiple:
        for key in note_to_hold_multiple[note]:
                keyboard.release(key)            

    elif raw_note < first_b_note and note in note_to_hold_singular:
            keyboard.release(note_to_hold_singular[note])  


def keyboard_press(note):
    if note in note_to_hold_singular:
        keyboard.press(note_to_hold_singular[note])
    elif note in note_to_hold_multiple:
        for key in note_to_hold_multiple[note]:
            keyboard.press(key)


def keyboard_release(note):
    if note in note_to_hold_singular:
        keyboard.release(note_to_hold_singular[note])
                   
    elif note in note_to_hold_multiple:
        for key in note_to_hold_multiple[note]:
                keyboard.release(key)

notes_log = []
play_lock = threading.Lock()

def play(filename, bpm=128, USER_INPUT=0, EVENT_CHANNEL=0, debug=False, status_callback=None):
    if not filename or not filename.strip():
        if debug:
            print("Empty filename")
        return False

    if not path.exists(filename):
        if debug:
            print("File not found")
        return False

    if not filename.lower().endswith(('.mid', '.midi')):
        if debug:
            print("Not a MIDI file")
        return False

    if status_callback:
        status_callback("idle")

    global notes_log
    notes_log.clear()
    thrd.clear()

    spt = 60 / (bpm * umidiparser.MidiFile(filename).miditicks_per_quarter) #seconds per tick

    if not play_lock.acquire(blocking=False):
        if debug:
            print("Midiparsing is running!")
        return False

    try:
        def playback():
            B_NOTES = [11+(octave*12) for octave in range(10)]
            first_b_note = None

            if status_callback:
                status_callback("playing")

            for event in umidiparser.MidiFile(filename):
                time.sleep(event.delta_miditicks * spt)
                if thrd.is_set():
                    break
    
                if event.status == umidiparser.NOTE_ON and event.velocity > 0 and event.channel == EVENT_CHANNEL:
                    raw_note = event.note - int(USER_INPUT)
                    note = get_note_key(raw_note)
                    notes_log.append(note)
                    if debug:
                        print(f'The list is: {notes_log}')
                    if raw_note in B_NOTES:
                        first_b_note = check_b_note_press(note, raw_note, first_b_note)
                    else:
                        keyboard_press(note)

                elif event.status == umidiparser.NOTE_OFF and event.channel == EVENT_CHANNEL:
                    raw_note = event.note - int(USER_INPUT)
                    note = get_note_key(raw_note)
                    if raw_note in B_NOTES and first_b_note is not None:
                        check_b_note_release(note, raw_note, first_b_note)
                    else:
                        keyboard_release(note)
                            
                elif event.status == umidiparser.END_OF_TRACK:
                    status_callback("completed")
                    if debug:
                        print("Midi end!")
                    break             
                
        threading.Thread(target=playback, daemon=True).start()
        return True
    finally:
        play_lock.release()
        

def stop_playback(event=None, debug=False,status_callback=None):
   
    thrd.set()
    with play_lock:
        if not notes_log:
            if debug:
                print("No notes")
            status_callback("stopped")
            return

        try:
            note = notes_log[-1]
            if debug:
                print(f"Quit note: {note}")
            if note in note_to_hold_singular:
                keyboard.press(note_to_hold_singular[note])
                keyboard.release(note_to_hold_singular[note])
            elif note in note_to_hold_multiple:
                for key in note_to_hold_multiple[note]:
                    keyboard.press(key)
                    keyboard.release(key)
            else:
                if debug:
                    print(f"Note {note} not found")
            status_callback("stopped")
                
        except Exception as e:
            print(f"Error releasing note {note}: {e}")
