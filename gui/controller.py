import os
from PySide6.QtCore import QThread, Signal
from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QDialog, QFileDialog
from assets.SmartStitchLogo import icon
from core.services import SettingsHandler
from core.utils.constants import OUTPUT_SUFFIX
from gui.process import GuiStitchProcess

SCRIPT_DIRECTORY = os.path.dirname(os.path.abspath(__file__))

# Define a custom QThread class for running the process asynchronously
class ProcessThread(QThread):
    progress = Signal(int, str)
    postProcessConsole = Signal(str)

    def __init__(self, parent):
        super(ProcessThread, self).__init__(parent)

    def run(self):
        process = GuiStitchProcess()
        process.run_with_error_msgs(
            input_path=MainWindow.inputField.text(),
            output_path=MainWindow.outputField.text(),
            use_waifu2x=MainWindow.waifu2xCheckbox.isChecked(),
            waifu2x_path=MainWindow.waifu2xPathField.text(),
            remove_noise=MainWindow.removeNoiseCheckbox.isChecked(),
            noise_level=MainWindow.noiseLevelSlider.value(),
            enlarge_photo=MainWindow.enlargePhotoCheckbox.isChecked(),
            scale_ratio=MainWindow.scaleRatioField.value(),
            profile=MainWindow.profileDropdown.currentText(),
            output_type=MainWindow.outputTypeDropdown.currentText(),
            mode=MainWindow.mode,
            processWaifu=MainWindow.processDropdown.currentText().lower(),
            status_func=self.progress.emit,
            console_func=self.postProcessConsole.emit,
        )

def initialize_gui():
    global MainWindow
    global settings
    global appVersion
    global appAuthor
    global processThread
    MainWindow = QUiLoader().load(os.path.join(SCRIPT_DIRECTORY, 'layout.ui'))
    settings = SettingsHandler()

    # Sets Window Title & Icon
    pixmap = QPixmap()
    pixmap.loadFromData(icon)
    appIcon = QIcon(pixmap)
    MainWindow.setWindowIcon(appIcon)
    appVersion = "3.1"
    appAuthor = "MechTechnology"
    MainWindow.setWindowTitle("SmartStitch By {0} [{1}]".format(appAuthor, appVersion))

    on_load()
    bind_signals()

    processThread = ProcessThread(MainWindow)
    processThread.progress.connect(update_process_progress)
    processThread.postProcessConsole.connect(update_postprocess_console)

    MainWindow.show()

def on_load(load_profiles=True):
    MainWindow.statusField.setText("Idle")
    MainWindow.statusProgressBar.setValue(0)
    MainWindow.outputTypeDropdown.setCurrentText(settings.load("output_type"))
    MainWindow.lossyField.setValue(settings.load("lossy_quality"))
    MainWindow.heightField.setValue(settings.load("split_height"))
    MainWindow.widthEnforcementDropdown.setCurrentIndex(settings.load("enforce_type"))
    MainWindow.customWidthField.setValue(settings.load("enforce_width"))
    MainWindow.detectorTypeDropdown.setCurrentIndex(settings.load("detector_type"))
    MainWindow.detectorSensitivityField.setValue(settings.load("senstivity"))
    MainWindow.scanStepField.setValue(settings.load("scan_step"))
    MainWindow.ignoreMarginField.setValue(settings.load("ignorable_pixels"))
    MainWindow.runProcessCheckbox.setChecked(settings.load("run_postprocess"))
    MainWindow.postProcessAppField.setText(settings.load("postprocess_app"))
    MainWindow.postProcessArgsField.setText(settings.load("postprocess_args"))
    MainWindow.waifu2xPathField.setText(settings.load("last_waifu2x_location"))
    MainWindow.waifu2xCheckbox.setChecked(settings.load("waifu2x"))
    MainWindow.noiseLevelSlider.setValue(settings.load("waifu2x_noise_level"))
    MainWindow.noiseLevelLabel.setText(f"Noise Level: {MainWindow.noiseLevelSlider.value()}")
    MainWindow.removeNoiseCheckbox.setChecked(settings.load("waifu2x_noise"))
    MainWindow.enlargePhotoCheckbox.setChecked(settings.load("waifu2x_enlarge"))
    MainWindow.scaleRatioField.setValue(settings.load("waifu2x_enlarge_level"))
    MainWindow.processDropdown.setCurrentText(settings.load("waifu2x_process"))
    output_type_changed(False)
    enforce_type_changed(False)
    detector_type_changed(False)
    waifu2x_changed()
    load_profile_dropdown(MainWindow.waifu2xPathField.text())
    if load_profiles:
        update_profiles_list()
        MainWindow.currentProfileDropdown.setCurrentIndex(settings.get_current_index())
        current_profile_changed(False)

def bind_signals():
    MainWindow.inputField.textChanged.connect(input_field_changed)
    MainWindow.browseButton.clicked.connect(browse_location)
    MainWindow.outputTypeDropdown.currentTextChanged.connect(output_type_changed)
    MainWindow.lossyField.valueChanged.connect(lossy_quality_changed)
    MainWindow.heightField.valueChanged.connect(split_height_changed)
    MainWindow.widthEnforcementDropdown.currentTextChanged.connect(enforce_type_changed)
    MainWindow.customWidthField.valueChanged.connect(custom_width_changed)
    MainWindow.detectorTypeDropdown.currentTextChanged.connect(detector_type_changed)
    MainWindow.detectorSensitivityField.valueChanged.connect(detector_sensitivity_changed)
    MainWindow.scanStepField.valueChanged.connect(scan_step_changed)
    MainWindow.ignoreMarginField.valueChanged.connect(ignorable_margin_changed)
    MainWindow.currentProfileDropdown.currentTextChanged.connect(current_profile_changed)
    MainWindow.currentProfileName.textChanged.connect(current_profile_name_changed)
    MainWindow.addProfileButton.clicked.connect(add_profile)
    MainWindow.removeProfileButton.clicked.connect(remove_profile)
    MainWindow.runProcessCheckbox.stateChanged.connect(run_postprocess_changed)
    MainWindow.browsePostProcessAppButton.clicked.connect(browse_postprocess_app)
    MainWindow.postProcessAppField.textChanged.connect(postprocess_app_changed)
    MainWindow.postProcessArgsField.textChanged.connect(postprocess_args_changed)
    MainWindow.startProcessButton.clicked.connect(launch_process_async)

    MainWindow.waifu2xCheckbox.stateChanged.connect(waifu2x_changed)
    MainWindow.browseWaifu2xPathButton.clicked.connect(browse_waifu2x_path)
    MainWindow.removeNoiseCheckbox.stateChanged.connect(remove_noise_changed)
    MainWindow.noiseLevelSlider.valueChanged.connect(noise_level_changed)
    MainWindow.enlargePhotoCheckbox.stateChanged.connect(enlarge_photo_changed)
    MainWindow.scaleRatioField.valueChanged.connect(enlarge_level_changed)
    MainWindow.profileDropdown.currentIndexChanged.connect(handleProfileChange)
    MainWindow.processDropdown.currentIndexChanged.connect(handleProcessChange)

def input_field_changed():
    input_path = MainWindow.inputField.text() or ""
    if input_path:
        MainWindow.outputField.setText(input_path + OUTPUT_SUFFIX)
    else:
        MainWindow.outputField.setText("")
    if os.path.exists(input_path):
        settings.save("last_browse_location", input_path)

def browse_location():
    start_directory = settings.load("last_browse_location")
    if not start_directory or not os.path.exists(start_directory):
        start_directory = os.path.expanduser("~")
    dialog = QFileDialog(
        MainWindow,
        'Select Input Directory Files',
        directory=start_directory,
        FileMode=QFileDialog.FileMode.Directory,
    )
    if dialog.exec_() == QDialog.Accepted:
        input_path = dialog.selectedFiles()[0] or ""
        MainWindow.inputField.setText(input_path)
        MainWindow.outputField.setText(input_path + OUTPUT_SUFFIX)

def output_type_changed(save=True):
    file_type = MainWindow.outputTypeDropdown.currentText()
    if save:
        settings.save("output_type", file_type)
    MainWindow.lossyWrapper.setHidden(file_type not in ['.jpg', '.webp'])
    if file_type not in ['.png', '.jpg', '.jpeg', '.tif', '.tiff', '.bmp', '.tga']:
        MainWindow.waifu2xCheckbox.setChecked(False)
        MainWindow.waifu2xCheckbox.setEnabled(False)
    else:
        MainWindow.waifu2xCheckbox.setEnabled(True)

def lossy_quality_changed():
    settings.save("lossy_quality", MainWindow.lossyField.value())

def split_height_changed():
    settings.save("split_height", MainWindow.heightField.value())

def enforce_type_changed(save=True):
    enforce_type = MainWindow.widthEnforcementDropdown.currentIndex()
    if save:
        settings.save("enforce_type", enforce_type)
    MainWindow.customWidthWrapper.setHidden(enforce_type != 2)

def custom_width_changed():
    settings.save("enforce_width", MainWindow.customWidthField.value())

def detector_type_changed(save=True):
    detector_type = MainWindow.detectorTypeDropdown.currentIndex()
    if save:
        settings.save("detector_type", detector_type)
    MainWindow.detectorSensitvityWrapper.setHidden(detector_type != 1)
    MainWindow.scanStepWrapper.setHidden(detector_type != 1)
    MainWindow.ignoreMarginWrapper.setHidden(detector_type != 1)

def detector_sensitivity_changed():
    settings.save("senstivity", MainWindow.detectorSensitivityField.value())

def scan_step_changed():
    settings.save("scan_step", MainWindow.scanStepField.value())

def ignorable_margin_changed():
    settings.save("ignorable_pixels", MainWindow.ignoreMarginField.value())

def update_profiles_list():
    profile_names = settings.get_profile_names()
    MainWindow.currentProfileDropdown.clear()
    MainWindow.currentProfileDropdown.addItems(profile_names)
    return len(profile_names)

def current_profile_changed(save=True):
    current_profile = MainWindow.currentProfileDropdown.currentIndex()
    if save:
        settings.set_current_index(current_profile)
        on_load(False)
    MainWindow.currentProfileName.setText(settings.get_current_profile_name())

def current_profile_name_changed():
    new_name = MainWindow.currentProfileName.text()
    settings.set_current_profile_name(new_name)
    current = MainWindow.currentProfileDropdown.currentIndex()
    MainWindow.currentProfileDropdown.setItemText(current, new_name)

def add_profile():
    profile_name = settings.add_profile()
    new_index = update_profiles_list() - 1
    MainWindow.currentProfileDropdown.setCurrentIndex(new_index)
    MainWindow.currentProfileName.setText(profile_name)

def remove_profile():
    current_profile = MainWindow.currentProfileDropdown.currentIndex()
    settings.remove_profile(current_profile)
    MainWindow.currentProfileDropdown.removeItem(current_profile)
    MainWindow.currentProfileDropdown.setCurrentIndex(0)

def run_postprocess_changed():
    settings.save("run_postprocess", MainWindow.runProcessCheckbox.isChecked())

def browse_postprocess_app():
    dialog = QFileDialog(
        MainWindow,
        'Select Post Process Application Directory',
        FileMode=QFileDialog.FileMode.ExistingFile,
    )
    if dialog.exec_() == QDialog.Accepted:
        input_path = dialog.selectedFiles()[0] or ""
        MainWindow.postProcessAppField.setText(input_path)

def postprocess_app_changed():
    settings.save("postprocess_app", MainWindow.postProcessAppField.text())

def postprocess_args_changed():
    settings.save("postprocess_args", MainWindow.postProcessArgsField.text())

def update_process_progress(percentage: int, message: str):
    MainWindow.statusField.setText(message)
    MainWindow.statusProgressBar.setValue(percentage)

def update_postprocess_console(message: str):
    MainWindow.processConsoleField.append(message)

def waifu2x_changed():
    use_waifu2x = MainWindow.waifu2xCheckbox.isChecked()
    settings.save("waifu2x", use_waifu2x)
    MainWindow.waifu2xPathField.setEnabled(use_waifu2x)
    MainWindow.browseWaifu2xPathButton.setEnabled(use_waifu2x)
    MainWindow.removeNoiseCheckbox.setEnabled(use_waifu2x)
    MainWindow.noiseLevelSlider.setEnabled(use_waifu2x)
    MainWindow.enlargePhotoCheckbox.setEnabled(use_waifu2x)
    MainWindow.scaleRatioField.setEnabled(use_waifu2x)

def browse_waifu2x_path():
    dialog = QFileDialog(
        MainWindow,
        'Select Waifu2X Path',
        FileMode=QFileDialog.FileMode.ExistingFile,
    )
    dialog.setNameFilter("waifu2x-caffe-cui.exe waifu2x-ncnn-vulkan.exe")
    if dialog.exec_() == QDialog.Accepted:
        input_path = dialog.selectedFiles()[0] or ""
        MainWindow.waifu2xPathField.setText(input_path)
        load_profile_dropdown(str(input_path))
        settings.save('last_waifu2x_location', input_path)

def load_profile_dropdown(path: str):
    if path.endswith("cui.exe"):
        MainWindow.profileDropdown.clear()
        MainWindow.profileDropdown.addItems(["anime_style_art", "anime_style_art_rgb", "photo", "ukbench", "upconv_7_anime_style_art_rgb", "upconv_7_photo", "upresnet10", "cunet"])
    elif path.endswith("vulkan.exe"):
        MainWindow.profileDropdown.clear()
        MainWindow.profileDropdown.addItems(["models-cunet", "models-upconv_7_anime_style_art_rgb", "models-upconv_7_photo"])
    MainWindow.profileDropdown.setCurrentText(settings.load("waifu2x_profile"))

def noise_level_changed():
    level = MainWindow.noiseLevelSlider.value()
    MainWindow.noiseLevelLabel.setText(f"Noise Level: {level}")
    settings.save("waifu2x_noise_level", level)

def enlarge_photo_changed():
    use_enlarge = MainWindow.enlargePhotoCheckbox.isChecked()
    settings.save("waifu2x_enlarge", use_enlarge)

def remove_noise_changed():
    use_noise = MainWindow.removeNoiseCheckbox.isChecked()
    settings.save("waifu2x_noise", use_noise)

def enlarge_level_changed():
    level_enlarge = MainWindow.scaleRatioField.value()
    settings.save("waifu2x_enlarge_level", level_enlarge)

def handleProfileChange():
    profile = MainWindow.profileDropdown.currentText()
    settings.save("waifu2x_profile", profile)

def handleProcessChange():
    processWaifu = MainWindow.processDropdown.currentText()
    settings.save("waifu2x_process", processWaifu)

def launch_process_async():
    MainWindow.processConsoleField.clear()
    remove_noise = MainWindow.removeNoiseCheckbox.isChecked()
    enlarge_photo = MainWindow.enlargePhotoCheckbox.isChecked()
    if remove_noise and enlarge_photo:
        MainWindow.mode = "noise_scale"
    elif remove_noise:
        MainWindow.mode = "noise"
    elif enlarge_photo:
        MainWindow.mode = "scale"
    else:
        MainWindow.mode = ""
    processThread.start()
