import os
import sys
import main
import platform
from PyQt5 import QtWidgets


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
    def __init__(self, parent=None):
        super().__init__(1)
        self.btnStep = QtWidgets.QPushButton("Step1", parent)
        self.btnStep.clicked.connect(lambda: parent.start_cmd(self))

class Step2(Step):
    def __init__(self, parent=None):
        super().__init__(2)
        self.btnStep = QtWidgets.QPushButton("Step2", parent)
        self.btnStep.clicked.connect(lambda: parent.start_cmd(self))

class Step3(Step):
    def __init__(self, parent=None):
        super().__init__(3)
        self.btnStep = QtWidgets.QPushButton("Step3", parent)
        self.btnStep.clicked.connect(lambda: parent.start_cmd(self))