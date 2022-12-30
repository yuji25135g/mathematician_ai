import os, sys

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from verifier.Formula import Formula
from verifier.Sequent import Sequent


def displaySeq(seq):
    leftFmls = []
    rightFmls = []
    for i in list(seq.left):
        leftFmls.append(i.string_formula)
    for i in list(seq.right):
        rightFmls.append(i.string_formula)

    seq_str = str(leftFmls) + " |- " + str(rightFmls)
    return seq_str
