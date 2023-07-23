from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication

from .controller import initialize_gui
from .stylesheet import load_styling

# Function to launch the application
def launch():
    # Create a QApplication instance
    app = QApplication([])

    # Enable the use of high DPI pixmaps for better resolution on high-density displays
    app.setAttribute(Qt.ApplicationAttribute.AA_UseHighDpiPixmaps)

    # Initialize the GUI components and set up event handlers
    initialize_gui()

    # Load and apply custom styling for the application's widgets
    app.setStyleSheet(load_styling())

    # Start the application's event loop, allowing it to respond to user interactions
    app.exec()