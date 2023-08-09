import math

from PyQt5.QtWidgets import QLabel
from qfluentwidgets import SettingCard, FluentIcon

from Modules.ModuleBase import CheckerBase
import string

from Background import mround

class CheckerProper(CheckerBase):
    _desc = "Usage of Capital Letters"
    tuneAccept = []
    freql = {}
    wnum = 0

    def run(self, callback=lambda x: None):
        self.cnt = 0
        self.corr = 0
        texts = self.compo.text.split("\n")
        while "" in texts:
            texts.remove("")
        pgc = 0
        for d in texts:
            pgc += 1
            flag = True
            t = d.split()
            wc = 0
            for word in t:
                wc += 1
                repl = word
                for p in string.punctuation:
                    repl = repl.replace(p, "")
                if flag:
                    self.cnt += 1
                    if 'A' <= repl[0] <= 'Z':
                        self.corr += 1
                    flag = False
                repl2 = word
                for p in string.punctuation:
                    if p in [".", "?", "!"]:
                        continue
                    repl2 = repl2.replace(p, "")
                if repl2.endswith(".") or repl2.endswith("?") or repl2.endswith("!"):
                    flag = True
                self.progress = (pgc - 1) / len(texts) + wc / len(word) / len(texts)
                callback(self)
        self.progress = 1
        callback(self)
        self.compo.setMark(self)

    def render(self, ui, wrapper):
        def newCard(title, cont, slt):
            settingCard = wrapper(
                lambda: SettingCard(FluentIcon.TAG, title, parent=slt)
            )
            if cont:
                wrapper(lambda: settingCard.hBoxLayout.addWidget(cont))
                wrapper(lambda: settingCard.hBoxLayout.addSpacing(19))
            return settingCard
        slot = wrapper(lambda: ui.interface.addGroup("Proper Capital Letters"))
        try:
            self.m = mround((self.corr - 1) / (self.cnt - 1) * 100, 2)
        except ZeroDivisionError:
            self.m = mround((self.corr / self.cnt)*100, 2)
        card = newCard("Marks: ", wrapper(lambda: QLabel(f"{self.m}/100")), slot)
        wrapper(lambda: slot.addSettingCard(card))
        card2 = newCard("No. of position needs to be capitalized", wrapper(lambda: QLabel(str(self.cnt))), slot)
        wrapper(lambda: slot.addSettingCard(card2))
        card3 = newCard("Capitalized", wrapper(lambda: QLabel(str(self.corr))), slot)
        wrapper(lambda: slot.addSettingCard(card3))
        wrapper(lambda: ui.interface.expand.addWidget(slot))
        print("Registered")

    def export(self):
        return {"Spelling Mistake": [
            ["Marks", self.m],
            ["No. of position needs to be capitalized", self.cnt],
            ["Capitalized", self.corr]
        ]}