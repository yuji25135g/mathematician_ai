import pytest
from typing import List
from Sequent import Sequent
from Formula import Formula
from inference import is_valid_inference


@pytest.mark.parametrize(
    ("assumption_sequent_list", "conclusion_sequent", "expected"),
    [
        # {A, B} |- {C}   {D, A} |- {C}
        # ----------------------------
        # {B | D, A} |- {C}
        (
            [
                Sequent({Formula("A"), Formula("B")}, {Formula("C")}),
                Sequent({Formula("D"), Formula("A")}, {Formula("C")}),
            ],
            Sequent({Formula("(B)|(D)"), Formula("A")}, {Formula("C")}),
            True,
        ),
        # {A, B} |- {C}   {D, A} |- {C}
        # ----------------------------
        # {B & D, A} |- {C}
        (
            [
                Sequent({Formula("A"), Formula("B")}, {Formula("C")}),
                Sequent({Formula("D"), Formula("A")}, {Formula("C")}),
            ],
            Sequent({Formula("(B)&(D)"), Formula("A")}, {Formula("C")}),
            False,
        ),
        # {A, B} |- {C}
        # ----------------------------
        # {B | D, A} |- {C}
        (
            [
                Sequent({Formula("A"), Formula("B")}, {Formula("C")}),
            ],
            Sequent({Formula("(B)|(D)"), Formula("A")}, {Formula("C")}),
            False,
        ),
        # {A, B} |- {F}   {D, A} |- {C}
        # ----------------------------
        # {B | D, A} |- {C}
        (
            [
                Sequent({Formula("A"), Formula("B")}, {Formula("F")}),
                Sequent({Formula("D"), Formula("A")}, {Formula("C")}),
            ],
            Sequent({Formula("(B)|(D)"), Formula("A")}, {Formula("C")}),
            False,
        ),
    ],
)
def test_Lor(assumption_sequent_list: List[Sequent], conclusion_sequent: Sequent, expected: bool):
    assert is_valid_inference(assumption_sequent_list, conclusion_sequent, "L|") == expected
