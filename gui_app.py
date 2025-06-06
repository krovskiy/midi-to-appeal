import qdarkstyle
import keyboard
import sys
import configparser
from core.chords_to_int import chords_to_int
from PySide6.QtGui import QFont
from PySide6.QtCore import Signal
from PySide6 import QtCore, QtWidgets, QtGui
from os import environ, name, path
environ["QT_API"] = "pyside6"


if name == "nt":
    from core.midireader_win import play, stop_playback
else:
    from core.midireader_linux import play, stop_playback


def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return path.join(sys._MEIPASS, relative_path)
    return path.join(path.abspath("."), relative_path)


class MainWindow(QtWidgets.QWidget):
    playback_status_changed = Signal(str)

    def __init__(self):
        '''Class instance'''
        super().__init__()
        self.reg_hotkeys = []
        self.setup_window()
        self.create_video()
        self.create_labels()
        self.create_widgets()
        self.style_widgets()
        self.channel_config()
        self.bpm_config()
        self.setup_layout()
        self.chord_combobox()
        self.mode_combobox()
        self.style_text()
        self.playback_status_changed.connect(self.update_status_label)
        self.default_midiplaying()

    def create_video(self):
        self.sprites = [resource_path('./materials/idle.gif'),
                        resource_path('./materials/playing.gif'),
                        resource_path('./materials/completed.gif'),
                        resource_path('./materials/stopped.gif')]
        self.status_animated = QtGui.QMovie(self.sprites[0])
        self.transform_video()

    def transform_video(self):
        org_size = self.status_animated.frameRect().size()
        max_size = QtCore.QSize(40, 40)
        scaled_size = org_size.scaled(max_size, QtCore.Qt.KeepAspectRatio)
        self.status_animated.setScaledSize(scaled_size)

    def setup_window(self):
        '''Window icon & title'''
        self.setWindowIcon(QtGui.QIcon(resource_path('icon.png')))
        self.setWindowTitle("midi-to-appeal")

    def eventFilter(self, obj, event):
        if event.type() == QtCore.QEvent.KeyPress:
            text = QtGui.QKeySequence(event.key()).toString()
            focused_widget = self.focusWidget()

            if focused_widget == self.start_key_assign:
                if self.check_valid(text):
                    self.start_key_assign.setText(text)
                    self.update_hotkeys()
                return True
            if focused_widget == self.stop_key_assign:
                if self.check_valid(text):
                    self.stop_key_assign.setText(text)
                    self.update_hotkeys()
                return True
        return super().eventFilter(obj, event)

    def create_widgets(self):
        '''Creates the buttons, boxes you see on window'''
        self.button = QtWidgets.QPushButton("Open file")
        self.text_edit = QtWidgets.QLineEdit()
        self.bpm_input = QtWidgets.QSpinBox()
        self.channel_input = QtWidgets.QSpinBox()
        self.select_chord = QtWidgets.QComboBox()
        self.select_mode = QtWidgets.QComboBox()
        self.start_key_assign = QtWidgets.QLineEdit()
        self.stop_key_assign = QtWidgets.QLineEdit()

        pixmap = QtGui.QPixmap(resource_path("./materials/si3lEuEp2Fk.png"))
        pixmap = pixmap.scaled(
            100,
            200,
            QtCore.Qt.KeepAspectRatio,
            QtCore.Qt.SmoothTransformation)
        self.label.setPixmap(pixmap)
        self.button.clicked.connect(self.open_file)

    def create_labels(self):
        '''Creates the text on the window'''
        self.text = QtWidgets.QLabel("midi-to-appeal")
        self.uptext = QtWidgets.QLabel("version 1.0")
        self.bottomtext = QtWidgets.QLabel("by dima and erica ⋆｡°✩")
        self.label = QtWidgets.QLabel()
        self.bpm_input_text = QtWidgets.QLabel("BPM:")
        self.channel_input_text = QtWidgets.QLabel("Channel:")
        self.select_chord_text = QtWidgets.QLabel("Chord:")
        self.select_mode_text = QtWidgets.QLabel("Mode:")
        self.status_text = QtWidgets.QLabel()
        self.status_label = QtWidgets.QLabel("Status:")
        self.start_key_assign_text = QtWidgets.QLabel("Start key:")
        self.stop_key_assign_text = QtWidgets.QLabel("Stop key:")
        self.status_label_animated = QtWidgets.QLabel()

    def style_text(self):
        font_family_style = f"font-family: '{font_family}';"
        widgets = [
            self.bpm_input_text,
            self.channel_input_text,
            self.select_chord_text,
            self.select_mode_text,
            self.status_label]
        key_widgets = [self.start_key_assign_text, self.stop_key_assign_text]
        keys = [self.start_key_assign, self.stop_key_assign]
        fixed = [
            self.bpm_input,
            self.channel_input,
            self.select_chord,
            self.select_mode,
            self.stop_key_assign,
            self.start_key_assign]

        for s in keys:
            s.setReadOnly(True)

        for k in key_widgets:
            k.setStyleSheet(f"QLabel{{{font_family_style}font-size:14px;}}")

        for w in widgets:
            w.setStyleSheet(f"QLabel{{{font_family_style}font-size:14px;}}")

        for f in fixed:
            f.setFixedSize(200, 22)

    def style_widgets(self):
        '''Styling the widgets (or making them 'beautiful' idk)'''
        font_family_style = f"font-family: '{font_family}';"

        self.text.setAlignment(QtCore.Qt.AlignCenter)
        self.text.setStyleSheet(
            f"QLabel{{{font_family_style}font-size: 32px;color: qlineargradient(x1:0, y1:0, x2:0, y2:110, stop:0 #04ff00, stop:1 #3700ff);margin-top: 30px;}}")
        self.uptext.setStyleSheet(
            f"QLabel{{{font_family_style}font-size: 15px;color: qlineargradient(x1:0, y1:32, x2:0, y2:0, stop:0 #04ff00, stop:1 #3700ff);margin-top: 12px;}}")
        self.bottomtext.setStyleSheet(
            f"QLabel{{{font_family_style}font-size: 12px;color: qlineargradient(x1:0, y1:120, x2:0, y2:0, stop:0 #3700ff, stop:1 #04ff00);margin-top:67px}}")

        self.status_label_animated.setMovie(self.status_animated)
        self.status_animated.start()

        self.installEventFilter(self)

        self.status_text.setText("Idle")
        self.status_text.setStyleSheet(
            f"QLabel{{{font_family_style}font-size: 18px;color:#808080;}}")

        self.button.setFont(QFont("Terminus", 12))
        self.button.setFixedHeight(22)
        self.text_edit.setFont(QFont("Terminus", 8))

    def setup_layout(self):
        '''Grid layout to setup the buttons, text, images'''
        layout = QtWidgets.QGridLayout(self)
        layout.setSpacing(8)
        layout.addWidget(self.label, 0, 0, alignment=QtCore.Qt.AlignTop)
        layout.addWidget(self.label, 0, 0, alignment=QtCore.Qt.AlignTop)
        layout.addWidget(self.uptext, 0, 1, alignment=QtCore.Qt.AlignTop | QtCore.Qt.AlignHCenter)
        layout.addWidget(self.bottomtext, 0, 1, alignment=QtCore.Qt.AlignTop | QtCore.Qt.AlignHCenter)
        layout.addWidget(self.text, 0, 1, alignment=QtCore.Qt.AlignTop | QtCore.Qt.AlignHCenter)
        layout.addWidget(self.channel_input_text, 1,0, alignment=QtCore.Qt.AlignTop | QtCore.Qt.AlignHCenter)
        layout.addWidget(self.channel_input, 1,1, alignment=QtCore.Qt.AlignTop | QtCore.Qt.AlignHCenter)
        layout.addWidget(self.bpm_input_text, 2,0, alignment=QtCore.Qt.AlignTop | QtCore.Qt.AlignHCenter)
        layout.addWidget(self.bpm_input, 2,1, alignment=QtCore.Qt.AlignTop | QtCore.Qt.AlignHCenter)
        layout.addWidget(self.select_chord_text,3,0, alignment=QtCore.Qt.AlignTop | QtCore.Qt.AlignHCenter)
        layout.addWidget(self.select_chord,3,1, alignment=QtCore.Qt.AlignTop | QtCore.Qt.AlignHCenter)
        layout.addWidget(self.select_mode_text,4,0, alignment=QtCore.Qt.AlignTop | QtCore.Qt.AlignHCenter)
        layout.addWidget(self.select_mode,4,1, alignment=QtCore.Qt.AlignTop | QtCore.Qt.AlignHCenter)
        layout.addWidget(self.start_key_assign_text,5,0, alignment=QtCore.Qt.AlignTop | QtCore.Qt.AlignHCenter)
        layout.addWidget(self.start_key_assign,5,1, alignment=QtCore.Qt.AlignCenter)
        layout.addWidget(self.stop_key_assign_text,6,0, alignment=QtCore.Qt.AlignTop | QtCore.Qt.AlignHCenter)
        layout.addWidget(self.stop_key_assign,6,1, alignment=QtCore.Qt.AlignCenter)
        layout.addWidget(self.status_label,7,0, alignment=QtCore.Qt.AlignHCenter)
        layout.addWidget(self.status_label_animated,7,1, alignment=QtCore.Qt.AlignRight | QtCore.Qt.AlignHCenter)
        layout.addWidget(self.status_text,7,1, alignment=QtCore.Qt.AlignHCenter)
        layout.addWidget(self.button, 8, 0, alignment=QtCore.Qt.AlignBottom)
        layout.addWidget(self.text_edit, 8, 1, alignment=QtCore.Qt.AlignBottom)

        self.setLayout(layout)

    def open_file(self):
        '''Open file logic'''
        file_dialog = QtWidgets.QFileDialog(self)
        file_dialog.setWindowTitle("Open file")
        file_dialog.setNameFilter("MIDI Files (*.mid *.midi)")
        file_dialog.setFileMode(QtWidgets.QFileDialog.FileMode.ExistingFile)
        file_dialog.setViewMode(QtWidgets.QFileDialog.ViewMode.Detail)
        if file_dialog.exec():
            selected_files = file_dialog.selectedFiles()
            self.text_edit.clear()
            self.text_edit.setText(selected_files[0])
            print("Selected File:", selected_files[0])
            return True
        return False

    def default_midiplaying(self):
        stop_key, start_key = self.config_load()
        self.start_key_assign.setText(start_key)
        self.stop_key_assign.setText(stop_key)
        self.register_hotkeys(start_key, stop_key)

    def clear_hotkeys(self):
        for hotkey in self.reg_hotkeys:
            try:
                keyboard.remove_hotkey(hotkey)
            except (ValueError, IOError, RuntimeError) as e:
                print(f"Specific error occurred: {e}")
        self.reg_hotkeys.clear()

    def check_valid(self, key):
        if not key or not isinstance(key, str):
            return False
        valid_keys = [
            'F1',
            'F2',
            'F3',
            'F4',
            'F5',
            'F6',
            'F7',
            'F8',
            'F9',
            'F10',
            'F11',
            'F12',
            '[',
            ']',
            ';']
        return key in valid_keys

    def register_hotkeys(self, start_key, stop_key):
        self.clear_hotkeys()
        if not self.check_valid(start_key) or not self.check_valid(stop_key):
            return False
        if stop_key == start_key:
            return False
        try:
            start_hotkey = keyboard.add_hotkey(start_key, self.play_arguments)
            stop_hotkey = keyboard.add_hotkey(stop_key, self.stop_arguments)
            self.reg_hotkeys = [start_hotkey, stop_hotkey]
            return True
        except BaseException:
            self.clear_hotkeys()
            return False

    def update_hotkeys(self):
        start_key = self.start_key_assign.text()
        stop_key = self.stop_key_assign.text()
        self.register_hotkeys(start_key,stop_key)

    def bpm_config(self):
        self.bpm_input.setRange(80, 180)
        self.bpm_input.setValue(128)

    def channel_config(self):
        self.channel_input.setRange(1, 16)
        self.channel_input.setValue(1)

    def play_arguments(self):
        smidi_path = self.text_edit.text().strip()
        bpm = self.bpm_input.value()
        chord = chords_to_int.get(self.select_chord.currentText())
        channel = int(self.channel_input.value() - 1)
        debug = False  # change this value for debug
        status_callback = self.playback_status_changed.emit
        if not self.isActiveWindow():
            play(smidi_path, bpm, chord, channel, debug, status_callback)
        else:
            print('program in focus')

    def stop_arguments(self):
        event = None
        debug = False  # change this value for debug
        status_callback = self.playback_status_changed.emit
        if not self.isActiveWindow():
            stop_playback(event, debug, status_callback)
        else:
            print('program in focus')

    def config_save(self):
        config = configparser.ConfigParser()
        config['midi-to-appeal'] = {'start_key': self.start_key_assign.text(),
                                    'stop_key': self.stop_key_assign.text()}
        with open('config.ini', 'w') as configFile:
            config.write(configFile)

    def config_load(self):
        config = configparser.ConfigParser()

        stop_key = 'F5'
        start_key = 'F4'

        if path.isfile('./config.ini'):
            try:
                config.read('config.ini')
                if config.has_section('midi-to-appeal'):
                    stop_key = config.get(
                        'midi-to-appeal', 'stop_key', fallback='F5')
                    start_key = config.get(
                        'midi-to-appeal', 'start_key', fallback='F4')
            except (configparser.Error, IOError) as e:
                print(f"Could not read config file: {e}")

        return stop_key, start_key

    def update_status_label(self, status):
        '''Checks the status from ./midireader_* and updates the GUI'''
        font_family_style = f"font-family: '{font_family}';"

        self.status_animated.stop()
        self.status_animated.deleteLater()

        if status == "idle":
            self.status_text.setText("Idle")
            self.status_text.setStyleSheet(
                f"QLabel{{font-size: 18px;{font_family_style};color:#808080;}}")
            self.status_animated = QtGui.QMovie(self.sprites[0])
        elif status == "playing":
            self.status_text.setText("Playing")
            self.status_text.setStyleSheet(
                f"QLabel{{font-size: 18px;{font_family_style};color:#7CFC00;}}")
            self.status_animated = QtGui.QMovie(self.sprites[1])
        elif status == "completed":
            self.status_text.setText("Completed")
            self.status_text.setStyleSheet(
                f"QLabel{{font-size: 18px;{font_family_style};;color:#7DF9FF;}} ")
            self.status_animated = QtGui.QMovie(self.sprites[2])
        elif status == "stopped":
            self.status_text.setText("Stopped")
            self.status_text.setStyleSheet(
                f"QLabel{{font-size: 18px;{font_family_style};;color:#FF0000;}}")
            self.status_animated = QtGui.QMovie(self.sprites[3])

        self.transform_video()
        self.status_label_animated.setMovie(self.status_animated)
        self.status_animated.start()

    def chord_combobox(self):
        '''Values for the chords combobox'''
        self.select_chord.addItems(['G# Minor / B Major',
                                    'A Minor / C Major',
                                    'A# Minor / C# Major',
                                    'B Minor / D Major',
                                    'C Minor / Eb Major',
                                    'C# Minor / E Major',
                                    'D Minor / F Major',
                                    'D# Minor / F# Major',
                                    'E Minor / G Major',
                                    'F Minor / Ab Major',
                                    'F# Minor / A Major',
                                    'G Minor / Bb Major'])

    def mode_combobox(self):
        self.select_mode.addItems(['Synth'])
        '''
        self.select_mode.addItems(['Synth', 'Drums'])

        dot dot dot

        code me! this is for the drums midi playback used by special characters

        '''


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    app.setStyleSheet(qdarkstyle.load_stylesheet())
    font = './fonts/TerminusTTF-4.49.3.ttf'
    font_id = QtGui.QFontDatabase.addApplicationFont(font)
    font_family = QtGui.QFontDatabase.applicationFontFamilies(font_id)[0]
    font = QtGui.QFont(font_family)
    font.setHintingPreference(QtGui.QFont.PreferFullHinting)
    font.setStyleStrategy(QtGui.QFont.PreferAntialias)
    app.setFont(font)
    widget = MainWindow()
    widget.setFixedSize(380, 420)
    widget.show()
    app.aboutToQuit.connect(widget.config_save)
    sys.exit(app.exec())
