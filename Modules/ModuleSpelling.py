from Modules.ModuleBase import CheckerBase, TunerWordSet
from Background import createQuery
import requests, re, time
import string

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
            self.runtimeCache[word] = result[0][0]
            return result[0][0]
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

    def run(self):
        text = self.compo.text.lower()
        for y in string.punctuation:
            if y == "'":
                continue
            text = text.replace(y, " ")
        listOfWord = [x.strip().strip("'") for x in text.split()]
        setOfWord = set(listOfWord)
        wrongList = [checkWord for checkWord in setOfWord if not self.wordcheck(checkWord)]
        self.words = setOfWord
        self.wrongs = set(wrongList)
        self.compo.setMark(self)

    def updateAllowance(self):
        self.tunedWrongs = self.wrongs.difference(self.tuneAccept[0]["Class"].val)