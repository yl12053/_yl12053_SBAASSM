from PyQt5.QtWidgets import QLabel
from qfluentwidgets import SettingCard, FluentIcon

from Modules.ModuleBase import CheckerBase
import string

from Background import mround
class CheckerUniqueness(CheckerBase):
    _desc = "Uniqueness"
    progress = 0
    tune = False
    tuneAccept = []

    runtimeCache = {}
    words = {}

    def run(self, callback=lambda x: None):
        self.progress = 0
        text = self.compo.text.lower()
        for y in string.punctuation:
            if y == "'":
                continue
            text = text.replace(y, " ")
        self.progress = 0.1
        listOfWord = [x.strip().strip("'") for x in text.split()]
        self.progress = 0.5
        setOfWord = set(listOfWord)
        self.progress = 0.8
        self.wordCnt = len(listOfWord)
        self.progress = 0.9
        self.uniqueCnt = len(setOfWord)
        self.prop = self.wordCnt - self.uniqueCnt
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
        slot = wrapper(lambda: ui.interface.addGroup("Uniqueness Check"))
        card = newCard("Marks: ", wrapper(lambda: QLabel(f"{mround((self.uniqueCnt - 1) * 100 / (self.wordCnt-1), 2)}/100")), slot)
        wrapper(lambda: slot.addSettingCard(card))
        card2 = newCard("No. of words", wrapper(lambda: QLabel(str(self.wordCnt))), slot)
        wrapper(lambda: slot.addSettingCard(card2))
        card3 = newCard("No. of unique words", wrapper(lambda: QLabel(str(self.uniqueCnt))), slot)
        wrapper(lambda: slot.addSettingCard(card3))
        wrapper(lambda: ui.interface.expand.addWidget(slot))
        print("Registered")

    def export(self):
        return {"Spelling Mistake": [
            ["Marks", mround((self.uniqueCnt - 1) * 100 / (self.wordCnt-1), 2)],
            ["No. of words", self.wordCnt],
            ["No. of unique words", self.uniqueCnt]
        ]}