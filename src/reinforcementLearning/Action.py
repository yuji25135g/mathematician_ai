from typing import Tuple, TypeAlias, Literal, Optional
from converter.fml2num import fml2num


InferenceStr: TypeAlias = Literal[
    "LW", "RW", "LC", "RC", "LX", "RX", "LF", "RT", "L&", "R&", "L|", "R|", "L>", "R>", "L!", "R!", "AX", "Emp"
]

inferenceTuple: Tuple[str] = (
    "LW",
    "RW",
    "LC",
    "RC",
    "LX",
    "RX",
    "LF",
    "RT",
    "L&",
    "R&",
    "L|",
    "R|",
    "L>",
    "R>",
    "L!",
    "R!",
    "AX",
    "Emp",
)


class Action:
    def __init__(self, inference: InferenceStr, formula1: Optional[str] = None, formula2: Optional[str] = None):
        self.inference = inference
        self.formula1 = formula1
        self.formula2 = formula2
        self.list = [inference, formula1, formula2]
        infIndex = inferenceTuple.index(inference)
        if formula1 == "":
            numFml1 = 0
        else:
            numFml1 = fml2num(self.formula1)
        if formula2 == "":
            numFml2 = 0
        else:
            numFml2 = fml2num(self.formula2)
        self.actionNum = (infIndex, numFml1, numFml2)
