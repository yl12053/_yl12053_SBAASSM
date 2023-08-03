from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtCore import Qt
from qfluentwidgets import InfoBar, InfoBarPosition
from FileReader import Support
import importlib
from qfluentwidgets import FluentIcon

def textChanged(ui):
    text = ui.TextEdit.toPlainText()
    ui.label_4.setText("Word Count: " + str(len(text.split())))
    ui.PushButton.setEnabled(len(text))
    ui.PrimaryPushButton.setEnabled(len(text))

def openFile(ui):
    files = QFileDialog.getOpenFileName(None, "Open file", "c:\\", " ".join(map(lambda x: "*."+x, Support.support)))
    if not files[0]:
        ui.PrimaryPushButton_3.setEnabled(False)
        return
    filename = files[0]
    fmt = filename.rsplit(".", 1)[1].lower()
    rtv, rtc = importlib.import_module("FileReader.%s"%fmt).process(filename)
    if rtv:
        InfoBar.error(
            title='Error on reading file',
            content=rtc,
            orient=Qt.Horizontal,
            isClosable=True,
            position=InfoBarPosition.TOP_RIGHT,
            duration=5000,
            parent=ui.mainWindow
        )
    else:
        ui.Page1Text = rtc
        ui.label_7.setText("File selected: %s\nFormat: %s\nWord Count: %d"%(filename, fmt, len(rtc.split())))
        ui.PrimaryPushButton_3.setEnabled(True)

def submitA(ui):
    ui.Page1Text = ui.TextEdit.toPlainText()
    submitB(ui)

def submitB(ui):
    ui.stackedWidget.setCurrentIndex(1)

def Init(obj):
    ui = obj.ui
    ui.PrimaryPushButton.setEnabled(False)
    ui.PushButton.setEnabled(False)
    ui.PrimaryPushButton_3.setEnabled(False)
    ui.TextEdit.textChanged.connect(lambda: textChanged(ui))
    ui.PushButton.clicked.connect(lambda: ui.TextEdit.setText(""))
    ui.PrimaryPushButton_2.clicked.connect(lambda: openFile(ui))
    ui.PrimaryPushButton.clicked.connect(lambda: submitA(ui))
    ui.PrimaryPushButton_3.clicked.connect(lambda: submitB(ui))
    obj.addmenu(ui.Homepage,FluentIcon.EDIT,"Homepage")