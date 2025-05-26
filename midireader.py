
import umidiparser
import keyboard
import threading
import time


thrd = threading.Event()

note_to_hold_singular = {
    'C': 'w',
    'E': 'd',
    'G': 's',
    'B': 'a',
    
}

note_to_hold_multiple = {
    'D': ['w','d'],
    'F': ['d','s'],
    'A': ['s','a'],
    'C': ['a','w']
}

def get_note_key(note):
    note_mod = note % 12
    if note_mod in {0,1,2,3,4,5,6,7,8,9,10,11}:
        note_mapping = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
        return note_mapping[note_mod]
    else:
        pass

notes_log = []

def play(filename, bpm=int, USER_INPUT=int):
    thrd.clear()
    sps = 60 / (bpm * umidiparser.MidiFile(filename).miditicks_per_quarter)
    def playback():
        for event in umidiparser.MidiFile(filename):
            sleep_duration = event.delta_miditicks*sps
            time.sleep(sleep_duration)
            if thrd.is_set():
                break
            if event.status == umidiparser.NOTE_ON and event.velocity > 0:
                bnote = get_note_key(event.note-int(USER_INPUT))
                print(f"The note: {bnote}")
                notes_log.append(bnote)
                print(f'The list is: {notes_log}')
                if bnote in note_to_hold_singular:
                    keyboard.press(note_to_hold_singular[bnote])
                elif bnote in note_to_hold_multiple:
                    for key in note_to_hold_multiple[bnote]:
                        keyboard.press(key)
            if event.status == umidiparser.NOTE_OFF:
                bnote = get_note_key(event.note-int(USER_INPUT))
                if bnote in note_to_hold_singular:
                    keyboard.release(note_to_hold_singular[bnote])
                elif bnote in note_to_hold_multiple:
                    for key in note_to_hold_multiple[bnote]:
                        keyboard.release(key)
            
    threading.Thread(target=playback, daemon=True).start()

def stop_playback(event=None):
    thrd.set()
    print(f"Quit note: {notes_log[-1]}")
    keyboard.press_and_release(note_to_hold_singular[notes_log[-1]]) #this is to fix the infinite moving 
    notes_log.clear()
