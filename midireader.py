
import umidiparser
import keyboard
import threading
import time
from note_mapping import note_to_hold_multiple, note_to_hold_singular

thrd = threading.Event()

def get_note_key(note):
    note_mod = note % 12
    if note_mod in {0,1,2,3,4,5,6,7,8,9,10,11}:
        note_mapping = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
        return note_mapping[note_mod]
    else:
        pass

notes_log = []

def play(filename, bpm=128, USER_INPUT=0, EVENT_CHANNEL=0):
    thrd.clear()
    sps = 60 / (bpm * umidiparser.MidiFile(filename).miditicks_per_quarter)

    def playback():
        C_list = [0, 12, 24, 36, 48, 60, 72, 84, 96, 108, 120]
        first_c_note = None

        for event in umidiparser.MidiFile(filename):
            time.sleep(event.delta_miditicks * sps)
            if thrd.is_set():
                break
   
            if event.status == umidiparser.NOTE_ON and event.velocity > 0 and event.channel == EVENT_CHANNEL:
                raw_note = event.note - int(USER_INPUT)
                bnote = get_note_key(raw_note)
                notes_log.append(bnote)
                print(f'The list is: {notes_log}')
                if raw_note in C_list:
                    if first_c_note is None:
                        first_c_note = raw_note
                    elif raw_note > first_c_note:
                        for key in note_to_hold_multiple[bnote]:
                            keyboard.press(key)
                    elif raw_note < first_c_note:
                        keyboard.press(note_to_hold_singular[bnote])

                if bnote in note_to_hold_singular:
                    keyboard.press(note_to_hold_singular[bnote])
                elif bnote in note_to_hold_multiple:
                    for key in note_to_hold_multiple[bnote]:
                        keyboard.press(key)

            elif event.status == umidiparser.NOTE_OFF and event.channel == EVENT_CHANNEL:
                raw_note = event.note - int(USER_INPUT)
                bnote = get_note_key(raw_note)
                if raw_note in C_list and first_c_note is not None:
                    if raw_note > first_c_note:
                        if bnote in note_to_hold_multiple:
                            for key in note_to_hold_multiple[bnote]:
                                keyboard.release(key)
                        continue
                    elif raw_note < first_c_note:
                        if bnote in note_to_hold_singular:
                            keyboard.release(note_to_hold_singular[bnote])
                        continue

                if bnote in note_to_hold_singular:
                    keyboard.release(note_to_hold_singular[bnote])
                elif bnote in note_to_hold_multiple:
                    for key in note_to_hold_multiple[bnote]:
                        keyboard.release(key)
            
    threading.Thread(target=playback, daemon=True).start()

def stop_playback(event=None):
    thrd.set()

    if not notes_log:
        print("No notes")
        return

    note = notes_log[-1]
    print(f"Quit note: {note}")

    try:
        if note in note_to_hold_singular:
            keyboard.press_and_release(note_to_hold_singular[note])
        elif note in note_to_hold_multiple:
            for key in note_to_hold_multiple[note]:
                keyboard.press_and_release(key)
        else:
            print(f"Note {note} not found")
            
    except Exception as e:
        print(f"Error releasing note {note}: {e}")
