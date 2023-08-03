import Base, Background
import UiInit
import os, importlib
from qfluentwidgets import qrouter

def wrapper():
    returnValue = [0]
    def main():
        from UI import GUI
        class BGUI(GUI):
            def exit(self):
                returnValue[0] = self.app.exec_()
            def refine(self):
                for suspect in sorted(os.listdir(list(UiInit.__path__)[0])):
                    if suspect.startswith("Init"):
                        print("Loading %s"%suspect)
                        moduleName = suspect.rsplit(".", 1)[0]
                        importlib.import_module("UiInit.%s"%moduleName)
                        getattr(UiInit, moduleName).Init(self)

            def launch(self):
                qrouter.setDefaultRouteKey(self.ui.stackedWidget, self.ui.Homepage.objectName())
                self.ui.stackedWidget.currentChanged.connect(self.interfaceChanged)
                self.ui.stackedWidget.setCurrentIndex(0)
                self.ui.NavigationBar.setCurrentItem(self.ui.Homepage.objectName())
                super().launch()

        MainWindow = BGUI()
        MainWindow.launch()


    def hook():
        return returnValue[0]

    return main, hook

Background.run(*(wrapper()))