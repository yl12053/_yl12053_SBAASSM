#Base class for a checker
class CheckerBase:
    tuneOpt = []

    def __init__(self, compo, callback = lambda x: None):
        self.compo = compo

    def run(self):
        raise NotImplementedError()

    def getDesc(self):
        return self._desc
        
#Base class for a tuner, preserved for future update
class Tuner:
    def __init__(self):
        raise NotImplementedError()

    def generate(self):
        raise NotImplementedError()

class TunerWordList(Tuner):
    def __init__(self, name, n=0, x=None):
        self.name = name
        self.val = []

class TunerWordSet(Tuner):
    def __init__(self, name, n=0, x=None):
        self.name = name
        self.val = set()

InitSetting = None
getNewSlot = None
