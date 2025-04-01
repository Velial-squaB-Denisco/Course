import os
import sys
import threading
import subprocess
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget

class MyWindow(QMainWindow):
    update_signal = QtCore.pyqtSignal(str)

    def __init__(self):
        super().__init__()

        self.setWindowTitle("My prog")
        self.setGeometry(300, 250, 350, 300)

        # Центральный виджет
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        # /// Label
        self.label = QtWidgets.QLabel("Iter++", self)
        main_layout.addWidget(self.label)

        # /// Горизонтальный макет для кнопок
        button_layoutH = QHBoxLayout()
        button_layoutV = QVBoxLayout()

        # /// Start
        self.btnStart = QtWidgets.QPushButton("Start", self)
        self.btnStart.clicked.connect(self.start)
        button_layoutH.addWidget(self.btnStart)

        # /// Stop
        self.btnStop = QtWidgets.QPushButton("Stop", self)
        self.btnStop.clicked.connect(self.stop)
        button_layoutH.addWidget(self.btnStop)

        # /// Reset
        self.btnReset = QtWidgets.QPushButton("Reset", self)
        self.btnReset.clicked.connect(self.reset)
        button_layoutV.addWidget(self.btnReset)

        # /// Step
        self.btnStep1 = QtWidgets.QPushButton("Step1", self)
        self.btnStep1.clicked.connect(lambda:self.run_cmd(1))
        button_layoutV.addWidget(self.btnStep1)

        self.btnStep2 = QtWidgets.QPushButton("Step2", self)
        self.btnStep2.clicked.connect(lambda:self.run_cmd(2))
        button_layoutV.addWidget(self.btnStep2)

        self.btnStep3 = QtWidgets.QPushButton("Step3", self)
        self.btnStep3.clicked.connect(lambda:self.run_cmd(3))
        button_layoutV.addWidget(self.btnStep3)

        main_layout.addLayout(button_layoutV)
        main_layout.addLayout(button_layoutH)

        # /// Output
        self.Output = QtWidgets.QTextEdit(self)
        self.Output.setReadOnly(True)
        main_layout.addWidget(self.Output)


        self.process = None
        self.thread = None
        self.running = False

        self.update_signal.connect(self.append_text)

    def reset(self):
        self.btnReset.setStyleSheet("background-color: gray;")
        self.btnStart.setStyleSheet("background-color: None;")
        self.btnStop.setStyleSheet("background-color: None;")

        self.append_text("Reset")

    def start(self):
        self.btnStart.setStyleSheet("background-color: green;")
        self.btnReset.setStyleSheet("background-color: None;")
        self.btnStop.setStyleSheet("background-color: None;")

        self.append_text("Start")

        if not self.running:
            self.running = True
            for i in range(3):
                self.thread = threading.Thread(target=self.run_cmd, args = (i + 1,))
                self.thread.start()

    def stop(self):
        self.btnStart.setStyleSheet("background-color: None;")
        self.btnReset.setStyleSheet("background-color: None;")
        self.btnStop.setStyleSheet("background-color: red;")

        self.append_text("Stop")

        if self.running and self.process:
            self.running = False
            self.process.terminate()

    def run_cmd(self, i):

        if getattr(sys, 'frozen', False):
            exe_dir = os.path.dirname(sys.executable)
            base_dir = os.path.abspath(os.path.join(exe_dir, '..'))
        else:
            base_dir = os.path.dirname(os.path.abspath(__file__))

        batch_file_path = os.path.join(base_dir, f'cmd{i}.bat')

        self.process = subprocess.Popen(
            [batch_file_path],
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding='cp1251',
            errors='replace'
        )

        for stdout_line in iter(self.process.stdout.readline, ""):
            if not self.running:
                break
            self.update_signal.emit(stdout_line)

        for stderr_line in iter(self.process.stderr.readline, ""):
            if not self.running:
                break
            self.update_signal.emit(stderr_line)

        self.process.stdout.close()
        self.process.stderr.close()
        self.process.wait()

    def append_text(self, text):
        self.Output.append(text)

    def closeEvent(self, event):
        self.running = False
        if self.thread is not None and self.thread.is_alive():
            self.stop(self)
            self.thread.join()
        event.accept()

def app():
    application = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(application.exec_())

if __name__ == "__main__":
    app()