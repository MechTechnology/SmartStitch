import os

from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QDialog, QFileDialog

from core.services import SettingsHandler
from core.utils.constants import OUTPUT_SUFFIX

SCRIPT_DIRECTORY = os.path.dirname(os.path.abspath(__file__))


def initalize_gui():
    global MainWindow
    global settings
    MainWindow = QUiLoader().load(os.path.join(SCRIPT_DIRECTORY, 'layout.ui'))
    settings = SettingsHandler()
    bind_signals()
    on_load()
    MainWindow.show()


def on_load():
    MainWindow.outputTypeDropdown.setCurrentText(settings.load("output_type"))
    MainWindow.lossyField.setValue(settings.load("lossy_quality"))
    MainWindow.heightField.setValue(settings.load("split_height"))
    MainWindow.widthEnforcementDropdown.setCurrentIndex(settings.load("enforce_type"))
    MainWindow.customWidthField.setValue(settings.load("enforce_width"))
    output_type_changed()
    enforce_type_changed()


def bind_signals():
    MainWindow.inputField.textChanged.connect(input_field_changed)
    MainWindow.browseButton.clicked.connect(browse_location)
    MainWindow.outputTypeDropdown.currentTextChanged.connect(output_type_changed)
    MainWindow.lossyField.valueChanged.connect(lossy_quality_changed)
    MainWindow.heightField.valueChanged.connect(split_height_changed)
    MainWindow.widthEnforcementDropdown.currentTextChanged.connect(enforce_type_changed)
    MainWindow.customWidthField.valueChanged.connect(custom_width_changed)


def input_field_changed():
    input_path = MainWindow.inputField.text() or ""
    if input_path:
        MainWindow.outputField.setText(input_path + OUTPUT_SUFFIX)
    else:
        MainWindow.outputField.setText("")


def browse_location():
    dialog = QFileDialog(
        MainWindow,
        'Select Input Directory Files',
        FileMode=QFileDialog.FileMode.Directory,
    )
    if dialog.exec_() == QDialog.Accepted:
        input_path = dialog.selectedFiles()[0] or ""
        MainWindow.inputField.setText(input_path)
        MainWindow.outputField.setText(input_path + OUTPUT_SUFFIX)


def output_type_changed():
    file_type = MainWindow.outputTypeDropdown.currentText()
    settings.save("output_type", file_type)
    if file_type in ['.jpg', '.webp']:
        MainWindow.lossyWrapper.setHidden(False)
    else:
        MainWindow.lossyWrapper.setHidden(True)


def lossy_quality_changed():
    settings.save("lossy_quality", MainWindow.lossyField.value())


def split_height_changed():
    settings.save("split_height", MainWindow.heightField.value())


def enforce_type_changed():
    enforce_type = MainWindow.widthEnforcementDropdown.currentIndex()
    settings.save("enforce_type", enforce_type)
    if enforce_type == 2:
        MainWindow.customWidthWrapper.setHidden(False)
    else:
        MainWindow.customWidthWrapper.setHidden(True)


def custom_width_changed():
    settings.save("enforce_width", MainWindow.customWidthField.value())
