from . import debug
import os
from pyqtkeybind import keybinder
from PyQt5 import uic
from PyQt5.QtCore import QAbstractEventDispatcher
from PyQt5.QtCore import QAbstractNativeEventFilter
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QMainWindow
import sys

class UI:

    def __init__(self):
        self.app = QApplication(sys.argv)
        ui_dir = os.path.dirname(os.path.abspath(__file__))
        ui_path = os.path.join(ui_dir, "window.ui")
        self.window = uic.loadUi(ui_path)
        assert isinstance(self.window, QMainWindow)
        self.window.setWindowFlag(Qt.Tool)
        self.window.setWindowFlag(Qt.WindowStaysOnTopHint)
        self.window.setAttribute(Qt.WA_QuitOnClose)
        self.stage_name_label = self.window.findChild(QLabel, "stage_name")
        assert self.stage_name_label
        self.stage_hint_label = self.window.findChild(QLabel, "stage_hint")
        assert self.stage_hint_label
        self.register_hotkey()
        self.window.show()

    def register_hotkey(self):
        keybinder.init()
        keybinder.register_hotkey(
            self.window.winId(),
            "Alt+F12",
            self.on_advance_stage_keyboard_event)
        self.event_filter = NativeEventFilter(keybinder)
        self.event_dispatcher = QAbstractEventDispatcher.instance()
        self.event_dispatcher.installNativeEventFilter(self.event_filter)

    def run(self):
        self.app.exec_()

    def apply_stage(self, stage):
        self.set_stage_name(stage.name)
        self.set_stage_hint(stage.hint)
        self.set_stage_color(stage.color)

    def set_stage_name(self, name):
        self.stage_name_label.setText(name)

    def set_stage_hint(self, hint):
        self.stage_hint_label.setText(hint)

    def set_stage_color(self, color):
        self.window.setStyleSheet("background-color: {}".format(color))

    def set_advance_stage_callback(self, callback):
        self.advance_stage_callback = callback

    def on_advance_stage_keyboard_event(self):
        self.advance_stage_callback()

class NativeEventFilter(QAbstractNativeEventFilter):

    def __init__(self, keybinder):
        self.keybinder = keybinder
        super().__init__()

    def nativeEventFilter(self, eventType, message):
        ret = self.keybinder.handler(eventType, message)
        return ret, 0
