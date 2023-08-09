import math

from PyQt5.QtWidgets import QLabel
from qfluentwidgets import SettingCard, FluentIcon

from Modules.ModuleBase import CheckerBase
import string
import bezier, sympy, numpy

from Background import mround

class CheckerWordCnt(CheckerBase):
    _desc = "No. of words"
    req = 600
    tuneAccept = []
    freql = {}
    wnum = 0
    nodes = numpy.asfortranarray([
        [0.0, 1.5, 0.5, 1.5],
        [0.0, 0.0, 1.0, 1.0]
    ])
    curve = bezier.Curve(nodes, degree = 3)
    expr = curve.implicitize()

    def setReq(self, req):
        self.req = req

    def run(self, callback=lambda x: None):
        text = self.compo.text.lower()
        for y in string.punctuation:
            if y == "'":
                continue
            text = text.replace(y, " ")
        self.progress = 0.5
        callback(self)
        listOfWord = [x.strip().strip("'") for x in text.split()]
        self.wnum = len(listOfWord)
        self.callback = 1
        callback(self)
        self.compo.setMark(self)

    def calculate(self):
        if self.wnum / self.req >= 1.5:
            self.mark = 1
        else:
            expr2 = self.expr.subs(sympy.Symbol('x'), self.wnum / self.req)
            roots = sympy.solveset(expr2, sympy.Symbol('y'), domain=sympy.S.Reals)
            for possible in roots:
                if 0 <= possible <= 1:
                    self.mark = possible.evalf()
                    break
            expr3 = self.expr.subs(sympy.Symbol('y'), 0.5)
            roots1 = sympy.solveset(expr3, sympy.Symbol('x'), domain=sympy.S.Reals)
            for poss in roots1:
                if 0 <= poss <= 1:
                    self.reqpass = math.ceil(poss * self.req)
                    break

    def render(self, ui, wrapper):
        self.calculate()
        def newCard(title, cont, slt):
            settingCard = wrapper(
                lambda: SettingCard(FluentIcon.TAG, title, parent=slt)
            )
            if cont:
                wrapper(lambda: settingCard.hBoxLayout.addWidget(cont))
                wrapper(lambda: settingCard.hBoxLayout.addSpacing(19))
            return settingCard
        slot = wrapper(lambda: ui.interface.addGroup("Number of words"))
        card = newCard("Marks: ", wrapper(lambda: QLabel(f"{mround(self.mark * 100, 2)}/100")), slot)
        wrapper(lambda: slot.addSettingCard(card))
        card2 = newCard("No. of words", wrapper(lambda: QLabel(str(self.wnum))), slot)
        wrapper(lambda: slot.addSettingCard(card2))
        card3 = newCard("Requirement of No. of words", wrapper(lambda: QLabel(str(self.req))), slot)
        wrapper(lambda: slot.addSettingCard(card3))
        card4 = newCard(
            "No. of words required to get pass on this item", wrapper(lambda: QLabel(str(self.reqpass))), slot
        )
        wrapper(lambda: slot.addSettingCard(card4))
        wrapper(lambda: ui.interface.expand.addWidget(slot))
        print("Registered")

    def export(self):
        return {"Spelling Mistake": [
            ["Marks", mround(self.mark * 100, 2)],
            ["No. of words", self.wnum],
            ["Requirement of No. of words", self.req],
            ["No. of words required to get pass on this item", self.reqpass]
        ]}