import pytest
from typing import List
from Formula import Formula
from Sequent import Sequent
from Node import Node


@pytest.mark.parametrize(
    ("node", "expected"),
    [
        # A |- A, B
        # ---------- (RW)
        # A |- A
        (
            Node(
                Sequent({Formula("A")}, {Formula("A"), Formula("B")}),
                "RW",
                [Node(Sequent({Formula("A")}, {Formula("A")}), "AX")],
            ),
            [Sequent({Formula("A")}, {Formula("A")})],
        ),
        # A |- A
        # ---------- (AX)
        (
            Node(
                Sequent({Formula("A")}, {Formula("A")}),
                "AX",
                [],
            ),
            [],
        ),
        # A |- B, A & !B
        # ------------------------- (R&)
        # A |- B, A    A |- B, !B
        (
            Node(
                Sequent({Formula("A")}, {Formula("B"), Formula("(A)&(!(B)")}),
                "R&",
                [
                    Node(Sequent({Formula("A")}, {Formula("B"), Formula("A")})),
                    Node(Sequent({Formula("A")}, {Formula("B"), Formula("!(A)")})),
                ],
            ),
            [
                Sequent({Formula("A")}, {Formula("B"), Formula("A")}),
                Sequent({Formula("A")}, {Formula("B"), Formula("!(A)")}),
            ],
        ),
    ],
)
def test_get_children_sequent_list(node: Node, expected: List[Sequent]):
    result = node.get_children_sequent_list()
    assert all(result[i].is_equal_to(expected[i]) for i in range(len(result)))
