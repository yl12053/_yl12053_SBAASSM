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
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"}
    def run(self):
        text = self.text
        listOfWord = text.split()
        listOfFinal = []
        for x in listOfWord:
            x = x.strip()
            for y in string.punctuation:
                if y == "'" or y == "-":
                    pass
                x = x.replace(y, "")
            for z in range(len(x)):
                if x[z] not in string.punctuation:
                    break
            x = x[z:]
            for z in range(
