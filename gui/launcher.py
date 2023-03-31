from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication

from .controller import initialize_gui
from .stylesheet import load_styling


def launch():
    app = QApplication([])
    app.setAttribute(Qt.ApplicationAttribute.AA_UseHighDpiPixmaps)
    initialize_gui()
    app.setStyleSheet(load_styling())
    app.exec()
