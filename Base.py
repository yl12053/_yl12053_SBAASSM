class CompositionBase:
    def __init__(self, text):
        self.text = text
        self._req = None
        self._marks = {}
        
    def setRequirement(self, num, flag):
        self._req = [num, flag]
        
    def getRequirement(self):
        return self._req

    def setMark(self, cb):
        self._marks[cb.__class__.__name__] = cb

    def getMark(self, crit=None):
        if crit:
            return self._marks[crit]
        return self._marks
