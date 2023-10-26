import Base, Background
import UiInit
import os, importlib
from qfluentwidgets import qrouter

#Wrapper for main procedure
#To be plug into Background.run
def wrapper():
    #Store returnValue into list, to emulate pass by pointer in Python
    returnValue = [0]
    def main():
        from UI import GUI
        class BGUI(GUI):
            #Custom exit function
            def exit(self, code=None):
                if code is None:
                    code = self.app.exec_()
                returnValue[0] = code

            #Module initialization
            def refine(self):
                for suspect in UiInit.members:
                    print("Loading %s"%suspect)
                    moduleName = suspect.rsplit(".", 1)[0]
                    importlib.import_module("UiInit.%s"%moduleName)
                    getattr(UiInit, moduleName).Init(self)

            #GUI Initialization procedure & Main loop
            def launch(self):
                qrouter.setDefaultRouteKey(self.ui.stackedWidget, self.ui.Homepage.objectName())
                self.ui.stackedWidget.currentChanged.connect(self.interfaceChanged)
                self.ui.stackedWidget.setCurrentIndex(0)
                self.ui.NavigationBar.setCurrentItem(self.ui.Homepage.objectName())
                super().launch()

        MainWindow = BGUI()
        #Hijack exit function
        Background.exitFunc = MainWindow.forceQuit
        MainWindow.launch()

    #Return value hook
    def hook():
        return returnValue[0]

    return main, hook

#Start program with wrapper(SQL initialization)
Background.run(*(wrapper()))
