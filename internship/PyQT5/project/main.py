import sys
import time
import threading
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget

class MyWindow(QMainWindow):
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
        self.btnStart.clicked.connect(self.control_loop)
        button_layout.addWidget(self.btnStart)

        # /// Pause Button
        self.btnPause = QtWidgets.QPushButton("Pause", self)
        self.btnPause.clicked.connect(self.pause_loop)
        button_layout.addWidget(self.btnPause)

        main_layout.addLayout(button_layout)

        # /// Output
        self.Output = QtWidgets.QTextEdit(self)
        self.Output.setReadOnly(True)
        main_layout.addWidget(self.Output)

        self.running = False
        self.stop = False
        self.i = 0
        self.a = 1
        self.thread = None

    # def control_loop(self):
    #     if not self.running:
    #         self.running = True
    #         self.paused = False
    #         self.thread = threading.Thread(target=self.iter)
    #         self.thread.start()
    #     elif self.paused:
    #         self.paused = False

    # def pause_loop(self):
    #     if self.running and not self.paused:
    #         self.paused = True

    # def iter(self):
    #     while self.running:
    #         if not self.paused:
    #             if self.i <= self.a:
    #                 QtCore.QMetaObject.invokeMethod(
    #                     self.Output, 
    #                     "append", 
    #                     QtCore.Q_ARG(str, str(self.i))
    #                 )
    #                 self.i += 1
    #                 self.a += 1
    #                 time.sleep(1)
    #             else:
    #                 self.running = False
    #         QtCore.QThread.msleep(100)

    def closeEvent(self, event):
        self.running = False
        if self.thread is not None and self.thread.is_alive():
            self.thread.join()
        event.accept()

def app():
    application = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(application.exec_())

if __name__ == "__main__":
    app()
