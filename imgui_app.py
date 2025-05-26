import sys
import keyboard
import qdarkstyle
from midireader import play, stop_playback
from PySide6 import QtCore, QtWidgets, QtGui
from PySide6.QtGui import QFont, QPixmap, QPainter, QBitmap, QPainterPath, QMovie
from PySide6.QtCore import QSize, Qt



class MyWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setup_window()
        self.create_widgets()
        self.style_widgets()
        self.setup_layout()
        self.midiplaying()
        

    def setup_window(self):
        self.setWindowIcon(QtGui.QIcon('icon.jpg'))
        self.setWindowTitle("midi-to-appeal")

    def create_widgets(self):
     
        self.text = QtWidgets.QLabel("midi-to-appeal")
        self.label = QtWidgets.QLabel()
        self.button = QtWidgets.QPushButton("Open file")
        self.textEdit = QtWidgets.QLineEdit()

        pixmap = QtGui.QPixmap("si3lEuEp2Fk.png")
        pixmap = pixmap.scaled(100, 200, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
        self.label.setPixmap(pixmap)

        self.button.clicked.connect(self.open_file)

    def style_widgets(self):
     
        self.text.setAlignment(QtCore.Qt.AlignCenter)
        self.text.setStyleSheet("QLabel{font-size: 30px;font-family: 'Terminus';color: qlineargradient(x1:0, y1:0, x2:0, y2:110, stop:0 #04ff00, stop:1 #3700ff);margin-top: 30px;}")

        self.button.setFont(QFont("Terminus", 12))
        self.textEdit.setFont(QFont("Terminus", 8))

    def setup_layout(self):
        layout = QtWidgets.QGridLayout(self)
        layout.setSpacing(3)

        layout.addWidget(self.label, 0, 0, alignment=QtCore.Qt.AlignTop)
        layout.addWidget(self.text, 0, 1, alignment=QtCore.Qt.AlignTop | QtCore.Qt.AlignHCenter)
        layout.addWidget(self.textEdit, 1, 1, alignment=QtCore.Qt.AlignBottom)
        layout.addWidget(self.button, 1, 0, alignment=QtCore.Qt.AlignBottom)

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
        keyboard.add_hotkey("F5", lambda: play(self.textEdit.text(),120,4))
        keyboard.add_hotkey("F6", stop_playback)
    

        
if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    app.setStyleSheet(qdarkstyle.load_stylesheet())

    widget = MyWidget()
    widget.setFixedWidth(380)
    widget.show()

    sys.exit(app.exec())