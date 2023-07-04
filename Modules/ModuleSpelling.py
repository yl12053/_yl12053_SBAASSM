from Modules.ModuleBase import CheckerBase, createQuery
import requests, re
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

class CheckerSpelling:
    runtimeCache = {}
    wordCnt = {}
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"}
    def wordcheck(self, word):
        requestObj = requests.get("https://dictionary.cambridge.org/search/direct", params = {
            "datasetsearch": "english",
            "q": word
        }, headers = self.headers)
        url = requestObj.url
        return "spellcheck" not in url
    def run(self):
        text = self.text
        for y in string.punctuation:
            if y == "'":
                continue
            text = text.replace(y, " ")
        listOfWord = [x.strip().strip("'") for x in text.split()]
