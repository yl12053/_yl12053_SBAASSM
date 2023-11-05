from PyQt5 import QtWidgets
from PyQt5.QtGui import QFontDatabase
import sys
from qfluentwidgets import qrouter, NavigationItemPosition
from UIM import Ui_MainWindow

#Initialization for UI (By creating a class)
class GUI:
    normProc = True

    #Onclick override - only when lock function pass, for thread-safety
    def defaultOnclick(self, func):
        if self.ui.lock():
            func()

    #Add custom entry to the sidebar (Preserved for future use)
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

    #Hook function, for whenever a switch of frame is triggered.
    def interfaceChanged(self, index):
        widget = self.ui.stackedWidget.widget(index)
        self.ui.NavigationBar.setCurrentItem(widget.objectName())
        qrouter.push(self.ui.stackedWidget, widget.objectName())

    #Init function
    def __init__(self):
        #Create window
        self.app = QtWidgets.QApplication(sys.argv)
        #Map font to Qt resource
        id = QFontDatabase.addApplicationFont("AGENCYR.ttf")
        families = QFontDatabase.applicationFontFamilies(id)
        #Link window
        self.window = QtWidgets.QMainWindow()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.window)
        self.ui.mainWindow = self.window
        #Global lock function (preserved, for future use, for thread-safe)
        self.ui.lock = lambda: True
        self.refine()

    refine = lambda self: None

    #Normal exit
    def exit(self, code=None):
        if code is None:
            code = self.app.exec_()
        sys.exit(code)

    #Termination
    def forceQuit(self, code=0):
        self.normProc = False
        self.app.exit(code)
        sys.exit(code)

    #Launch
    def launch(self):
        self.window.show()
        if self.normProc:
            self.exit()
