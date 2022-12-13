from typing import List, Tuple, TypeAlias, Literal, Dict, Optional, Union
import os, sys

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from actionGenerator.generateAction import generateUnAction
from actionGenerator.displaySequent import displaySeq
from verifier.Formula import Formula
from verifier.Sequent import Sequent

seq1 = Sequent({Formula("C"), Formula("B")}, {Formula("!(A)")})
seq2 = Sequent({Formula("C"), Formula("B")}, {Formula("!(A)")})

a = (1, 2, 3)
b = (1, 2, 3)
print(a == b)
