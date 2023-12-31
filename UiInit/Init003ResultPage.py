from PyQt5.QtWidgets import QAction
from qfluentwidgets import RoundMenu
from FileReader import txt

uiObj = None
slots = []

#init function
def Init(obj):
    global uiObj
    uiObj = obj.ui

    #Dropdown button for exporting
    menu = RoundMenu()
    exportToTxt = QAction("Plain Text File", parent=menu)
    exportToTxt.triggered.connect(lambda: txt.export(obj.ui.compoend))
    menu.addAction(exportToTxt)
    obj.ui.primaryDropDownPushButton.setMenu(menu)
    #Back to home
    obj.ui.PushButton_2.clicked.connect(lambda: obj.ui.stackedWidget.setCurrentIndex(0))
