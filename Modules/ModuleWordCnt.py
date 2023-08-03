from Modules.ModuleBase import CheckerBase
import string

class CheckerWordCnt(CheckerBase):
    tuneAccept = []
    freql = {}
    wnum = 0

    def run(self):
        text = self.compo.text.lower()
        for y in string.punctuation:
            if y == "'":
                continue
            text = text.replace(y, " ")
        listOfWord = [x.strip().strip("'") for x in text.split()]
        self.wnum = len(listOfWord)
        for d in listOfWord:
            if d in self.freql:
                self.freql[d] += 1
            else:
                self.freql[d] = 1
        self.compo.setMark(self)

    def estimate(self):
        cnt = 0
        for d in self.freql.values():
            cnt += d - 1
        return 1 - (cnt / self.wnum)