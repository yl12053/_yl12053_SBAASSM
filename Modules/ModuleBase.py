class CheckerBase:
    tuneOpt = []

    def __init__(self, compo):
        self.compo = compo
        self.run()

    def run(self):
        raise NotImplementedError()

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