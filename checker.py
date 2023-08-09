from Background import running
from Modules.ModuleSpelling import CheckerSpelling
from Modules.ModuleUniqueness import CheckerUniqueness
from Modules.ModuleWordCnt import CheckerWordCnt
from Modules.ModuleProper import CheckerProper
from Base import CompositionBase
from Background import threadWrapper

class UCheckerSpelling(CheckerSpelling):
    def wordcheck(self, word):
        assert running
        print("Check word: %s"%word)
        return super().wordcheck(word)

procedures = [UCheckerSpelling, CheckerUniqueness, CheckerWordCnt, CheckerProper]

@threadWrapper
def check(ui, wrapper, end):
    global running
    compo = CompositionBase(ui.Page1Text)
    ui.compoend = compo
    for i in range(len(procedures)):
        if running:
            def callback(obj):
                wrapper(lambda: ui.ProgressBar.setValue(int(round((i + obj.progress)*100/len(procedures)))))
            obj = procedures[i](compo, callback)
            ui.label_9.setText("Current Checking: %s" % obj.getDesc())
            obj.run(callback)
            obj.render(ui, wrapper)
    wrapper(ui.interface.show)
    wrapper(lambda: ui.stackedWidget.setCurrentIndex(3))
    end()