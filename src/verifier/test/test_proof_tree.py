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
        # --------------------- (R|)
        #   |- A | !A
        (
            ProofTree(
                Node(
                    Sequent(set(), {Formula("(A)|(!(A))")}),
                    "R|",
                    [
                        Node(
                            Sequent(set(), {Formula("A"), Formula("!(A)")}),
                            "R!",
                            [Node(Sequent({Formula("A")}, {Formula("A")}))],
                        )
                    ],
                )
            ),
            True,
        ),
        # -------- (AX)  ---------- (AX)
        # A |- A          B |- B
        # --------- (RW) ---------- (LW)
        # A |- B, A       B, A |- B
        #               ------------ (R!)
        #                 A |- B, !B
        # ------------------------------ (R&)
        # A |- B, A & !B
        # ------------------------------ (L!)
        # A, !(A & !B) |- B
        # ------------------------------ (R>)
        # !(A & !B) |- A -> B
        (
            ProofTree(
                Node(
                    Sequent({Formula("!((A)&(!(B)))")}, {Formula("(A)>(B)")}),
                    "R>",
                    [
                        Node(
                            Sequent({Formula("A"), Formula("!((A)&(!(B)))")}, {Formula("B")}),
                            "L!",
                            [
                                Node(
                                    Sequent({Formula("A")}, {Formula("B"), Formula("(A)&(!(B))")}),
                                    "R&",
                                    [
                                        Node(
                                            Sequent({Formula("A")}, {Formula("B"), Formula("A")}),
                                            "RW",
                                            [Node(Sequent({Formula("A")}, {Formula("A")}))],
                                        ),
                                        Node(
                                            Sequent({Formula("A")}, {Formula("B"), Formula("!(B)")}),
                                            "R!",
                                            [
                                                Node(
                                                    Sequent({Formula("B"), Formula("A")}, {Formula("B")}),
                                                    "LW",
                                                    [Node(Sequent({Formula("B")}, {Formula("B")}))],
                                                )
                                            ],
                                        ),
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
