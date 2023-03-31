from qdarktheme import load_stylesheet

LIGHT_STYLE_SHEET = """
QPushButton {
    color: rgb(40, 83, 65);
    background: rgba(38, 238, 159, 1);
}
QPushButton:!window {
    color: rgb(40, 83, 65);
    background: rgba(38, 238, 159, 1);
}
QWidget {
    background: #ffffff;
    color: #000000;
    selection-background-color: rgb(38, 120, 65);
    selection-color: #ffffff;
}
QWidget:item:selected,
QWidget:item:checked
{
    background: rgb(38, 120, 65);
    color: #ffffff;
}
QPushButton:default {
    color: #ffffff;
    background: #43e689;
}
QPushButton:hover,
QPushButton:flat:hover {
    background: rgba(38, 238, 159, 0.666);
}
QPushButton:pressed,
QPushButton:flat:pressed,
QPushButton:checked:pressed,
QPushButton:flat:checked:pressed {
    background: rgba(38, 238, 159, 0.333);
}
QPushButton:checked,
QPushButton:flat:checked {
    background: rgba(38, 238, 159, 0.933);
}
QPushButton:default:hover {
    background: rgba(38, 238, 159, 0.666);
}
QPushButton:default:pressed {
    background: rgba(38, 238, 159, 0.333);
}
QPushButton:default:disabled {
    background: #dbe1de;
}

QTabBar::tab:hover {
    background: rgba(38, 238, 159, 0.666);
}
QTabBar::tab:selected {
    color: rgb(40, 83, 65);
    background: rgba(38, 238, 159, 0.333);
}
QTabBar::tab:selected:disabled {
    background: #dbe1de;
    color: #babdc2;
}
QTabBar::tab:top:selected {
    border-bottom: 2px solid rgba(38, 238, 159, 1);
}
QTabBar::tab:top:hover {
    border-color: rgba(38, 238, 159, 1);
}
QTabBar::tab:top:selected:disabled {
    border-color: #dbe1de;
}
QTabBar::tab:selected:hover:enabled{
    color: rgb(40, 83, 65);
    background: rgba(38, 238, 159, 0.333);
}
QTabBar::tab:selected:enabled {
    color: rgb(40, 83, 65);
    background: rgba(38, 238, 159, 0.333);
}
QTabBar::tab:bottom {
    border-top: 2px solid #dbe1de;
}
QTabBar::tab:bottom:selected {
    border-top: 2px solid rgba(38, 238, 159, 1);
}
QTabBar::tab:bottom:hover {
    border-color: rgba(38, 238, 159, 1);
}
QTabBar::tab:bottom:selected:disabled {
    border-color: #dbe1de;
}
QTabBar::tab:left {
    border-right: 2px solid #dbe1de;
}
QTabBar::tab:left:selected {
    border-right: 2px solid rgba(38, 238, 159, 1);
}
QTabBar::tab:left:hover {
    border-color: rgba(38, 238, 159, 1);
}
QTabBar::tab:left:selected:disabled {
    border-color: #dbe1de;
}
QTabBar::tab:right {
    border-left: 2px solid #dbe1de;
}
QTabBar::tab:right:selected {
    border-left: 2px solid rgba(38, 238, 159, 1);
}
QTabBar::tab:right:hover {
    border-color: rgba(38, 238, 159, 1);
}
QTabBar::tab:right:selected:disabled {
    border-color: #dbe1de;
}
QGroupBox {
    border: 1px solid #dbe1de;
}
QLineEdit,
QAbstractSpinBox {
    border: 1px solid #dbe1de;
}
QLineEdit:focus,
QAbstractSpinBox:focus {
    border: 1px solid rgba(38, 238, 159, 1);
}
QComboBox {
    border: 1px solid #dbe1de;
    background: rgba(255.000, 255.000, 255.000, 0.000);
}
QComboBox:focus,
QComboBox:open {
    border: 1px solid rgba(38, 238, 159, 1);
}
QComboBox::drop-down {
    border: none;
    padding-right: 4px;
}
QComboBox::item:selected {
    border: none;
    background: rgb(38, 120, 65);
    color: #ffffff;
}
QComboBox QAbstractItemView {
    background: #ffffff;
    border: 1px solid #dbe1de;
    selection-background-color: rgb(38, 120, 65);
    selection-color: #ffffff;
}
QTextEdit:focus,
QTextEdit:selected,
QPlainTextEdit:focus,
QPlainTextEdit:selected {
    border: 1px solid rgba(38, 238, 159, 1);
    selection-background-color: rgb(38, 120, 65);
}
QProgressBar::chunk {
    background: rgba(38, 238, 159, 1);
}
QCheckBox,
QRadioButton {
    border-top: 2px solid transparent;
    border-bottom: 2px solid transparent;
}
QCheckBox:!window,
QRadioButton:!window {
    background: transparent;
}
QCheckBox:hover,
QRadioButton:hover {
    border-bottom: 2px solid transparent;
}
QCheckBox::indicator:checked,
QGroupBox::indicator:checked,
QAbstractItemView::indicator:checked {
    image: url(./assets/CheckboxHighlight.svg);
}

"""


def load_styling():
    main_styles = load_stylesheet("light")
    return main_styles + LIGHT_STYLE_SHEET
