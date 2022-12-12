import os, sys

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from actionGenerator.generateAction import generateUnAction
from actionGenerator.displaySequent import displaySeq
from verifier.Formula import Formula
from verifier.Sequent import Sequent

seq1 = Sequent({Formula("C"), Formula("B")}, {Formula("!(A)")})

print(displaySeq(seq1))

result = generateUnAction(seq1, [["L!", "!(B)", ""], ["R!", "A", ""]], [0.2, 0.3, 0.5])
print(result[1])
print(displaySeq(result[0]))
