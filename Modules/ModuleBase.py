class CheckerBase:
    def __init__(self, compo):
        self.compo = compo
        self.run()

    def run(self):
        raise NotImplemented()

createQuery = None
