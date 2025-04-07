import os
import sys
import platform
import subprocess
from threading import Thread
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget

class Step:
    def __init__(self, step_number):
        self.step_number = step_number

    def run_script(self):
        if getattr(sys, 'frozen', False):
            exe_dir = os.path.dirname(sys.executable)
            base_dir = os.path.abspath(os.path.join(exe_dir, '..'))
        else:
            base_dir = os.path.dirname(os.path.abspath(__file__))

        scripts_dir = os.path.join(base_dir, 'scripts')
        if platform.system().lower() == "windows":
            script_path = os.path.join(scripts_dir, f'cmd{self.step_number}.bat')
        else:
            script_path = os.path.join(scripts_dir, f'cmd{self.step_number}.sh')

        return script_path

class Step1(Step):
    def __init__(self):
        super().__init__(1)

class Step2(Step):
    def __init__(self):
        super().__init__(2)

class Step3(Step):
    def __init__(self):
        super().__init__(3)

class MyWindow(QMainWindow):
    update_signal = QtCore.pyqtSignal(str)
    progress_updated = QtCore.pyqtSignal(int)
    reset_progress = QtCore.pyqtSignal()

    def __init__(self):
        super().__init__()


        #////////////  \\\\\\\\\\\\

        self.running = True
        self.process = None
        self.thread = None

        #////////////  \\\\\\\\\\\\

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
        self.btnStep1.clicked.connect(lambda: self.start_cmd(Step1()))
        button_layoutV.addWidget(self.btnStep1)

        self.btnStep2 = QtWidgets.QPushButton("Step2", self)
        self.btnStep2.clicked.connect(lambda: self.start_cmd(Step2()))
        button_layoutV.addWidget(self.btnStep2)

        self.btnStep3 = QtWidgets.QPushButton("Step3", self)
        self.btnStep3.clicked.connect(lambda: self.start_cmd(Step3()))
        button_layoutV.addWidget(self.btnStep3)

        main_layout.addLayout(button_layoutV)
        main_layout.addLayout(button_layoutH)

        # /// ProgressBar
        self.progressBar = QtWidgets.QProgressBar(self)
        main_layout.addWidget(self.progressBar)

        # /// Output
        self.Output = QtWidgets.QTextEdit(self)
        self.Output.setReadOnly(True)
        main_layout.addWidget(self.Output)

        self.append_text(platform.system().lower())

        self.progress_updated.connect(self.update_progress)
        self.reset_progress.connect(self.reset_progress_bar)

        for btn in [self.btnStep1, self.btnStep2, self.btnStep3]:
            btn.setEnabled(True)
            btn.setStyleSheet("background-color: None;")

    def reset_progress_bar(self):
        self.progressBar.setValue(0)

    def update_progress(self, value):
        self.progressBar.setValue(value)

    def reset(self):
        if self.running and self.process:
            self.running = False
            self.process.wait()
            self.process.terminate()

        self.Output.clear()
        self.progressBar.setValue(0)

        for btn in [self.btnStep1, self.btnStep2, self.btnStep3]:
            btn.setEnabled(True)
            btn.setStyleSheet("background-color: None;")

    def start(self):
        if self.running and self.process:
            self.running = False
            self.process.terminate()
            self.append_text("Stop")

        self.running = True
        self.append_text("Start")
        self.thread = Thread(target=self.run_cmds_sequentially)
        self.thread.start()


    def run_cmds_sequentially(self):
        for step_class in [Step1, Step2, Step3]:
            if not self.running:
                break
            self.run_cmd(step_class())

    def start_cmd(self, step_instance):
        if self.running and self.process:
            self.running = False
            self.process.terminate()
            self.append_text("Stop")

        self.running = True
        self.thread = Thread(target=self.run_cmd, args=(step_instance,))
        self.thread.start()


    def stop(self):
        self.append_text("Stop")
        if self.running and self.process:
            self.running = False
            self.process.terminate()

        self.btnStart.setEnabled(True)
        self.btnReset.setEnabled(True)
        self.btnStep1.setEnabled(True)
        self.btnStep2.setEnabled(True)
        self.btnStep3.setEnabled(True)

    def run_cmd(self, step_instance):
        self.reset_progress.emit()
        script_path = step_instance.run_script()
        self.append_text(script_path)
        getattr(self, f'btnStep{step_instance.step_number}').setStyleSheet("background-color: yellow;")

        self.btnStart.setEnabled(False)
        self.btnReset.setEnabled(False)
        self.btnStep1.setEnabled(False)
        self.btnStep2.setEnabled(False)
        self.btnStep3.setEnabled(False)

        self.process = subprocess.Popen(
            [script_path],
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding='cp866',
            errors='replace'
        )

        self.read_output(self.process.stdout, "stdout")
        self.read_output(self.process.stderr, "stderr")

        if self.running and self.process:
            getattr(self, f'btnStep{step_instance.step_number}').setStyleSheet("background-color: green;")
        else:
            getattr(self, f'btnStep{step_instance.step_number}').setStyleSheet("background-color: red;")

        self.btnStart.setEnabled(True)
        self.btnReset.setEnabled(True)
        self.btnStep1.setEnabled(True)
        self.btnStep2.setEnabled(True)
        self.btnStep3.setEnabled(True)

    def read_output(self, stream, stream_type):
        for line in iter(stream.readline, ""):
            if not self.running:
                break
            line_strip = line.strip()
            self.append_text(f"{stream_type}: {line_strip}")
            
            if "Step" in line_strip:
                parts = line_strip.split()
                if len(parts) >= 4 and parts[0] == "Step":
                    step_str = parts[-1]
                    try:
                        current_step = int(step_str)
                        total_steps = 10
                        percent = int((current_step / total_steps) * 100)
                        self.progress_updated.emit(percent)
                    except ValueError:
                        pass
        stream.close()

    def append_text(self, text):
        self.Output.append(text)

    def closeEvent(self, event):
        self.running = False
        if self.thread is not None and self.thread.is_alive():
            self.stop()
            self.thread.join()
        event.accept()

def app():
    application = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(application.exec_())

if __name__ == "__main__":
    app()