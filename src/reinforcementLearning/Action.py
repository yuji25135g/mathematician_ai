from typing import Tuple, TypeAlias, Literal, Optional
from converter.fml2num import fml2num
from converter.seq2num import seq2num
from verifier.Sequent import Sequent


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
    def __init__(
        self,
        inference: InferenceStr,
        seq1: Sequent,
        seq2: Sequent,
        formula1: Optional[str] = None,
        formula2: Optional[str] = None,
    ):
        self.inference = inference
        self.seq1 = seq1
        self.seq2 = seq2
        self.formula1 = formula1
        self.formula2 = formula2
        self.list = [inference, seq1.__str__(), seq2.__str__(), formula1, formula2]
        infIndex = inferenceTuple.index(inference)
        numSeq1 = seq2num(seq1)
        numSeq2 = seq2num(seq2)
        if formula1 == "":
            numFml1 = 0
        else:
            numFml1 = fml2num(self.formula1)
        if formula2 == "":
            numFml2 = 0
        else:
            numFml2 = fml2num(self.formula2)
        self.actionNum = (infIndex, numSeq1, numSeq2, numFml1, numFml2)
