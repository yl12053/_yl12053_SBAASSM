from PyQt5.QtWidgets import QLabel

from Modules.ModuleBase import CheckerBase, TunerWordSet
from Modules import ModuleBase
from qfluentwidgets import FluentIcon, SettingCard
from Background import createQuery
import requests, time
import string

from Background import mround

#Create a SQLite table
#Name: Spelling
#Columns:
#    (text) Word
#    (int) Correct
#    (float/real) Timeout
#Primary key: Word
initSql = """
create table if not exists Spelling (
    Word text,
    Correct integer,
    Timeout real,
    primary key (Word)
)
"""
createQuery(initSql)


class CheckerSpelling(CheckerBase):
    _desc = "Spelling Mistake"
    progress = 0
    tune = True
    tuneAccept = [{"Name": "Word allowance", "Class": TunerWordSet("Word allowance")}]

    runtimeCache = {}
    words = {}
    wrongs = {}
    tunedWrongs = {}
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/114.0.0.0 Safari/537.36"}

    def wordcheck(self, word):
        if word in self.runtimeCache:
            return self.runtimeCache[word]
        selectSql = "select Correct, Timeout from Spelling where Word = ?"
        result = createQuery(selectSql, [word])
        if len(result) > 0 and result[0][1] <= time.time():
            self.runtimeCache[word] = bool(result[0][0])
            return bool(result[0][0])
        requestObj = requests.get("https://dictionary.cambridge.org/search/direct/", params={
            "datasetsearch": "english",
            "q": word
        }, headers=self.headers)
        url = requestObj.url
        checkResult = "spellcheck" not in url
        updateSql = "insert or replace into Spelling values (?, ?, ?)"
        createQuery(updateSql, [word, checkResult, time.time() + 2628000])
        self.runtimeCache[word] = checkResult
        return checkResult

    def run(self, callback=lambda x: None):
        self.progress = 0
        text = self.compo.text.lower()
        for y in string.punctuation:
            if y == "'":
                continue
            text = text.replace(y, " ")
        listOfWord = [x.strip().strip("'") for x in text.split()]
        setOfWord = set(listOfWord)
        wrongList = []
        for checkWord in setOfWord:
            if not self.wordcheck(checkWord):
                wrongList.append(checkWord)
                print("Wrong: %s"%checkWord)
            self.progress += 1/len(setOfWord)
            callback(self)
        print(self.runtimeCache)
        self.progress = 1
        callback(self)
        self.words = setOfWord
        self.wrongs = set(wrongList)
        self.occurance = {k: listOfWord.count(k) for k in self.wrongs}
        self.compo.setMark(self)

    def updateAllowance(self):
        self.tunedWrongs = self.wrongs.difference(self.tuneAccept[0]["Class"].val)

    def render(self, ui, wrapper):
        def newCard(title, cont, slt):
            settingCard = wrapper(
                lambda: SettingCard(FluentIcon.TAG, title, parent=slt)
            )
            if cont:
                wrapper(lambda: settingCard.hBoxLayout.addWidget(cont))
                wrapper(lambda: settingCard.hBoxLayout.addSpacing(19))
            return settingCard
        slot = wrapper(lambda: ui.interface.addGroup("Spelling Check"))
        lbl = wrapper(lambda: QLabel(f"{mround((len(self.words) - len(self.wrongs)) * 100 / len(self.words), 2)}/100"))
        card = newCard("Marks: ", lbl, slot)
        wrapper(lambda: slot.addSettingCard(card))
        settingCard2 = wrapper(lambda: ui.interface.types(FluentIcon.TAG, "No. of wrong words", None, parent=slot))
        if len(self.wrongs):
            lab = wrapper(lambda: QLabel("Wrong Words: ", parent=settingCard2.view))
            wrapper(lambda: settingCard2.viewLayout.addWidget(lab))
            for wds in self.wrongs:
                scard = wrapper(lambda: SettingCard(FluentIcon.TAG, wds, parent=settingCard2.view))
                wrapper(lambda: scard.hBoxLayout.addWidget(QLabel(str(self.occurance[wds]))))
                wrapper(lambda: scard.hBoxLayout.addSpacing(19))
                wrapper(lambda: settingCard2.viewLayout.addWidget(scard))
        else:
            lab = wrapper(lambda: QLabel("There isn't any spelling mistake.", parent=settingCard2.view))
            wrapper(lambda: settingCard2.viewLayout.addWidget(lab))
        wrapper(lambda: settingCard2.adjustViewSize())
        wrapper(lambda: settingCard2.addWidget(QLabel(str(len(self.wrongs)))))
        wrapper(lambda: slot.addSettingCard(settingCard2))
        wrapper(lambda: ui.interface.expand.addWidget(slot))
        print("Registered")

    def export(self):
        return {"Spelling Mistake": [
            ["Marks", mround((len(self.words) - len(self.wrongs)) * 100 / len(self.words), 2)],
            ["No. of wrong words", len(self.wrongs)],
        ]}
