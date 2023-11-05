from PyQt5.QtWidgets import QFileDialog, QApplication, QWidget, QAction
from PyQt5.QtCore import Qt
from FileReader import Support
import importlib, threading
from qfluentwidgets import FluentIcon
import checker
import queue
import os
from qfluentwidgets import (
    InfoBar,
    InfoBarPosition,
    ExpandSettingCard,
    ScrollArea,
    ExpandLayout,
    SettingCardGroup,
)
from PyQt5.QtCore import pyqtSignal

#Call back function to update label and allow composition submit if and only if text is begin inputted
def textChanged(ui):
    text = ui.TextEdit.toPlainText()
    ui.label_4.setText("Word Count: " + str(len(text.split())))
    ui.PushButton.setEnabled(len(text))
    ui.PrimaryPushButton.setEnabled(len(text))

#procedure for file open and read
def openFile(ui):
    #Call OS' Native File Dialog, filetype was limited here
    files = QFileDialog.getOpenFileName(None, "Open file", os.getcwd(), " ".join(map(lambda x: "*."+x, Support.support)))
    #No file is selected
    if not files[0]:
        #Not allowing submit
        ui.PrimaryPushButton_3.setEnabled(False)
        return
    #Get filename
    filename = files[0]
    #Get file type
    fmt = filename.rsplit(".", 1)[1].lower()
    #Try to import corresponding file reader by filetype
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

#Inherited from qfluentwidgets.ExpandSettingCard
#Aim to expose private method _adjustViewSize to public
class Exposure(ExpandSettingCard):
    par = None
    def adjustViewSize(self):
        self._adjustViewSize()

#Visual element to render output
class ViewScroll(ScrollArea):

    types = Exposure
    addsig = pyqtSignal()
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.localwidget = QWidget()
        self.expand = ExpandLayout(self.localwidget)
        self.expand.setAlignment(Qt.AlignTop)
        self.itms = []

    def add(self, ico, title):
        self.itms.append(Exposure(ico, title, None, self.localwidget))
        return self.itms[-1]

    def addGroup(self, title):
        self.itms.append(SettingCardGroup(title, self.localwidget))
        return self.itms[-1]

    def show(self):
        self.resize(1000, 800)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setViewportMargins(0, 0, 0, 20)
        self.setWidget(self.localwidget)
        self.setWidgetResizable(True)
        self.expand.setSpacing(28)
        self.expand.setContentsMargins(60, 0, 60, 0)
        for d in self.itms:
            self.expand.addWidget(d)

#a pre-requisite submit procedure for manual input to convert textarea into str type
def submitA(ui):
    ui.Page1Text = ui.TextEdit.toPlainText()
    submitB(ui)

#remove all possible 
def submitB(ui):
    if hasattr(ui, "interface"):
        ui.horizontalLayout_7.removeWidget(ui.interface)
        ui.interface.setParent(None)
    ui.interface = ViewScroll(ui.widget)
    ui.horizontalLayout_7.addWidget(ui.interface)
    ui.stackedWidget.setCurrentIndex(1)
    #Custom task object
    class TObj:
        def __init__(self, func):
            #Function
            self.f = func
            #Return
            self.r = None
            #Error
            self.e = False
            #Task have done
            self.d = False

        #Get result, blocking
        def getResult(self):
            while not self.d:
                pass
            if self.e:
                raise self.r
            else:
                return self.r

        #Set result, calling from thread
        def setResult(self, r, e):
            self.r = r
            self.e = e
            self.d = True
    q = queue.Queue()

    #Function wrapper of a cross-thread call where the function execute in current thread
    def wrap(f):
        obj = TObj(f)
        q.put(obj)
        return obj.getResult()

    #End function, by putting a None
    def end():
        q.put(None)

    #Thread start
    threading.Thread(target=checker.check, args=(ui, wrap, end)).start()
    while True:
        try:
            f = q.get_nowait()
            if f is None:
                break
            try:
                f.setResult(f.f(), False)
            except Exception as e:
                f.setResult(e, True)
        except queue.Empty:
            pass
        QApplication.processEvents()

#Init function for page 1, called from outside (as a module)
def Init(obj):
    ui = obj.ui
    #Widgets initialization
    ui.PrimaryPushButton.setEnabled(False)
    ui.PushButton.setEnabled(False)
    ui.PrimaryPushButton_3.setEnabled(False)
    ui.TextEdit.textChanged.connect(lambda: textChanged(ui))
    #Clear
    ui.PushButton.clicked.connect(lambda: ui.TextEdit.setText(""))
    #Submit and read file
    ui.PrimaryPushButton_2.clicked.connect(lambda: openFile(ui))
    ui.PrimaryPushButton.clicked.connect(lambda: submitA(ui))
    ui.PrimaryPushButton_3.clicked.connect(lambda: submitB(ui))
    #Add to sidebar
    obj.addmenu(ui.Homepage,FluentIcon.EDIT,"Homepage")
