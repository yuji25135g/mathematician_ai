from Formula import Formula
from Sequent import Sequent

def displaySeq(seq):
    leftFmls=[]
    rightFmls=[]
    for i in list(seq.left):
        leftFmls.append(i.string_formula)
    for i in list(seq.right):
        rightFmls.append(i.string_formula)

    seq_str = str(leftFmls)+" |- "+str(rightFmls)
    return seq_str
