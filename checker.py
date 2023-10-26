from Background import running
#Module walk-through
from Modules.ModuleSpelling import CheckerSpelling
from Modules.ModuleUniqueness import CheckerUniqueness
from Modules.ModuleWordCnt import CheckerWordCnt
from Modules.ModuleProper import CheckerProper
from Base import CompositionBase
from Background import threadWrapper

#Inherited and overwrited workcheck, for thread-safe
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
            #callback procedure to update progressbar
            def callback(obj):
                wrapper(lambda: ui.ProgressBar.setValue(int(round((i + obj.progress)*100/len(procedures)))))
            #Walk-through procedures and run
            obj = procedures[i](compo, callback)
            ui.label_9.setText("Current Checking: %s" % obj.getDesc())
            obj.run(callback)
            #Render output (report)
            obj.render(ui, wrapper)
    wrapper(ui.interface.show)
    #switch to result page
    wrapper(lambda: ui.stackedWidget.setCurrentIndex(3))
    end()
