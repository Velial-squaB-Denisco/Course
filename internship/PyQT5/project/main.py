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
        button_layout = QHBoxLayout()

        # /// Start Button
        self.btnStart = QtWidgets.QPushButton("Start", self)
        self.btnStart.clicked.connect(self.start)
        button_layout.addWidget(self.btnStart)

        # /// Pause Button
        self.btnPause = QtWidgets.QPushButton("Stop", self)
        self.btnPause.clicked.connect(self.stop)
        button_layout.addWidget(self.btnPause)

        main_layout.addLayout(button_layout)

        # /// Output
        self.Output = QtWidgets.QTextEdit(self)
        self.Output.setReadOnly(True)
        main_layout.addWidget(self.Output)

        self.process = None
        self.thread = None
        self.running = False

        self.update_signal.connect(self.append_text)

    def start(self):
        if not self.running:
            self.running = True
            self.thread = threading.Thread(target=self.run_cmd)
            self.thread.start()

    def stop(self):
        if self.running and self.process:
            self.running = False
            self.process.terminate()

    def run_cmd(self):

        if getattr(sys, 'frozen', False):
            exe_dir = os.path.dirname(sys.executable)
            base_dir = os.path.abspath(os.path.join(exe_dir, '..'))
        else:
            base_dir = os.path.dirname(os.path.abspath(__file__))

        batch_file_path = os.path.join(base_dir, 'cmd.bat')

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