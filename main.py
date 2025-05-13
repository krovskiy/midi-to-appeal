
import umidiparser
import keyboard
import time
import threading

thrd = threading.Event()

USER_INPUT = 4

filename = "./serpents.mid"

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

def play(filename):
    thrd.clear()

    def playback():
        for event in umidiparser.MidiFile(filename).play():

            if thrd.is_set():
                break

            if event.status == umidiparser.NOTE_ON:
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

keyboard.add_hotkey("F5", lambda: play(filename))
keyboard.add_hotkey("F6", stop_playback)




#note = note_to_key.get()
#note = note_to_key.get('C')
#print(note)

#keyboard.press('space')
#keyboard.release('space')


def main():
    pass


if __name__ == "__main__":
    main()

