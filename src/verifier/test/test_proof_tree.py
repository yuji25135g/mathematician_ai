import pytest
from typing import List
from Formula import Formula
from Sequent import Sequent
from Node import Node
from ProofTree import ProofTree


@pytest.mark.parametrize(
    ("proof_tree", "expected"),
    [
        # -------- (AX)
        # A |- A
        # -------- (L!)
        # !A, A |-
        # -------- (R!)
        # A |- !!A
        (
            ProofTree(
                Node(
                    Sequent({Formula("A")}, {Formula("!(!(A))")}),
                    "R!",
                    [
                        Node(
                            Sequent({Formula("!(A)"), Formula("A")}, set()),
                            "L!",
                            [Node(Sequent({Formula("A")}, {Formula("A")}))],
                        )
                    ],
                )
            ),
            True,
        ),
        # -------(AX)
        # A |- A
        # --------- (R!)
        #   |- A, !A
        # ------------- (R|1)
        #   |- A, A | !A
        # -------------------- (R|2)
        #   |- A | !A, A | !A
        # --------------------- (RC)
        #   |- A | !A
        (
            ProofTree(
                Node(
                    Sequent(set(), {Formula("(A)|(!(A))")}),
                    "RC",
                    [
                        Node(
                            Sequent(set(), {Formula("(A)|(!(A))"), Formula("(A)|(!(A))")}),
                            "R|2",
                            [
                                Node(
                                    Sequent(set(), {Formula("A"), Formula("(A)|(!(A))")}),
                                    "R|1",
                                    [
                                        Node(
                                            Sequent(set(), {Formula("A"), Formula("!(A)")}),
                                            "R!",
                                            [Node(Sequent({Formula("A")}, {Formula("A")}))],
                                        )
                                    ],
                                )
                            ],
                        )
                    ],
                )
            ),
            True,
        ),
    ],
)
def test_verifier(proof_tree: ProofTree, expected: bool):
    assert proof_tree.verify() == expected
