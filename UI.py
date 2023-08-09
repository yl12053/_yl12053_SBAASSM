from PyQt5 import QtWidgets
from PyQt5.QtGui import QFontDatabase
import sys
from qfluentwidgets import qrouter, NavigationItemPosition
from UIM import Ui_MainWindow

class GUI:
    normProc = True

    def defaultOnclick(self, func):
        if self.ui.lock():
            func()

    def addmenu(self, interface, icon, text, onclick=None, position=NavigationItemPosition.TOP):
        if onclick is None:
            onclick = self.defaultOnclick
        switch = lambda: self.ui.stackedWidget.setCurrentWidget(interface)
        self.ui.NavigationBar.addItem(
            routeKey=interface.objectName(),
            icon=icon,
            text=text,
            onClick=onclick(switch),
            position=position,
            tooltip=text
        )

    def interfaceChanged(self, index):
        widget = self.ui.stackedWidget.widget(index)
        self.ui.NavigationBar.setCurrentItem(widget.objectName())
        qrouter.push(self.ui.stackedWidget, widget.objectName())
    def __init__(self):
        self.app = QtWidgets.QApplication(sys.argv)
        id = QFontDatabase.addApplicationFont("AGENCYR.ttf")
        families = QFontDatabase.applicationFontFamilies(id)
        self.window = QtWidgets.QMainWindow()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.window)
        self.ui.mainWindow = self.window
        self.ui.lock = lambda: True
        self.refine()

    refine = lambda self: None

    def exit(self, code=None):
        if code is None:
            code = self.app.exec_()
        sys.exit(code)

    def forceQuit(self, code=0):
        self.normProc = False
        self.app.exit(code)
        sys.exit(code)

    def launch(self):
        self.window.show()
        if self.normProc:
            self.exit()