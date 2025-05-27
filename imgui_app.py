import sys
import keyboard
import qdarkstyle
from os import environ
environ["QT_API"] = "pyside6"
from qtpy.QtCore import QCoreApplication
import qdarkstyle
from midireader import play, stop_playback
from PySide6 import QtCore, QtWidgets, QtGui
from PySide6.QtGui import QFont
from note_mapping import chords_to_int

class MyWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setup_window()
        self.create_labels()
        self.create_widgets()
        self.style_widgets()
        self.channel_config()
        self.bpm_config()
        self.setup_layout()
        self.midiplaying()
        self.chord_combobox()

    def setup_window(self):
        self.setWindowIcon(QtGui.QIcon('icon.jpg'))
        self.setWindowTitle("midi-to-appeal")

    def create_widgets(self):
        self.button = QtWidgets.QPushButton("Open file")
        self.textEdit = QtWidgets.QLineEdit()
        self.bpm_input = QtWidgets.QSpinBox()
        self.channel_input = QtWidgets.QSpinBox()
        self.select_chord = QtWidgets.QComboBox()

        pixmap = QtGui.QPixmap("si3lEuEp2Fk.png")
        pixmap = pixmap.scaled(100, 200, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
        self.label.setPixmap(pixmap)
        self.button.clicked.connect(self.open_file)
    
    def create_labels(self):
        self.text = QtWidgets.QLabel("midi-to-appeal")
        self.uptext = QtWidgets.QLabel("version 1.0")
        self.bottomtext = QtWidgets.QLabel("by dima and erica ⋆｡°✩")
        self.label = QtWidgets.QLabel()
        self.bpm_input_text = QtWidgets.QLabel("BPM:")
        self.channel_input_text = QtWidgets.QLabel("Channel:")
        self.select_chord_text = QtWidgets.QLabel("Chord:")


    def style_widgets(self):
     
        self.text.setAlignment(QtCore.Qt.AlignCenter)
        self.text.setStyleSheet("QLabel{font-size: 30px;font-family: 'Terminus';color: qlineargradient(x1:0, y1:0, x2:0, y2:110, stop:0 #04ff00, stop:1 #3700ff);margin-top: 30px;}")
        self.uptext.setStyleSheet("QLabel{font-size: 13px;font-family: 'Terminus';color: qlineargradient(x1:0, y1:20, x2:0, y2:800, stop:0 #04ff00, stop:1 #3700ff);}")
        self.bottomtext.setStyleSheet("QLabel{font-size: 10px;font-family: 'Terminus';color: qlineargradient(x1:0, y1:120, x2:0, y2:0, stop:0 #3700ff, stop:1 #04ff00);margin-top:67px}")

        widgets = [self.bpm_input_text, self.channel_input_text, self.select_chord_text]

        for w in widgets:
            w.setStyleSheet("QLabel{font-family: 'Terminus'; font-size:14px;}")

        fixed = [self.bpm_input, self.channel_input, self.select_chord]
        for f in fixed:
            f.setFixedSize(200,20)
            
        self.button.setFont(QFont("Terminus", 12))
        self.button.setFixedHeight(22)
        self.textEdit.setFont(QFont("Terminus", 8))

    def setup_layout(self):
        layout = QtWidgets.QGridLayout(self)
        layout.setSpacing(5)
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
        layout.addWidget(self.textEdit, 4, 1, alignment=QtCore.Qt.AlignBottom)
        layout.addWidget(self.button, 4, 0, alignment=QtCore.Qt.AlignBottom)

        self.setLayout(layout)

    def open_file(self):
        file_dialog = QtWidgets.QFileDialog(self)
        file_dialog.setWindowTitle("Open file")
        file_dialog.setNameFilter("MIDI Files (*.mid *.midi)")
        file_dialog.setFileMode(QtWidgets.QFileDialog.FileMode.ExistingFile)
        file_dialog.setViewMode(QtWidgets.QFileDialog.ViewMode.Detail)
        if file_dialog.exec():
            selected_files = file_dialog.selectedFiles()
            self.textEdit.clear()
            self.textEdit.insert(selected_files[0])
            print("Selected File:", selected_files[0])

    def midiplaying(self):
        keyboard.add_hotkey("F5", self.play_arguments)
        keyboard.add_hotkey("F6", stop_playback)
    
    def bpm_config(self):
        self.bpm_input.setRange(80,180)
        self.bpm_input.setValue(128)

    def channel_config(self):
        self.channel_input.setRange(1,16)
        self.channel_input.setValue(1)
    
    def play_arguments(self):
        midi_path = self.textEdit.text()
        bpm = self.bpm_input.value()
        chord = chords_to_int.get(self.select_chord.currentText())
        channel = int(self.channel_input.value()-1)
        play(midi_path,bpm,chord,channel)

    
    def chord_combobox(self):
        self.select_chord.addItems(['A Minor / C Major',
        'A# Minor / C# Major',
        'B Minor / D Major',
        'C Minor / D# Major',
        'C# Minor / E Major',
        'D Minor / F Major',
        'D# Minor / F# Major',
        'E Minor / G Major',
        'F Minor / G# Major',
        'F# Minor / A Major',
        'G Minor / A# Major',
        'G# Minor / B Major'])
            

        
if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    app.setStyleSheet(qdarkstyle.load_stylesheet())

    widget = MyWidget()
    widget.setFixedWidth(380)
    widget.show()

    sys.exit(app.exec())