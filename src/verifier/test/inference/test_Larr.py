import pytest
from typing import List
from Sequent import Sequent
from Formula import Formula
from inference import is_valid_inference


@pytest.mark.parametrize(
    ("assumption_sequent_list", "conclusion_sequent", "expected"),
    [
        # {A} |- {B, C}  {D, E} |- {F}
        # ----------------------------
        # {C -> D, A, E} |- {B, F}
        (
            [
                Sequent({Formula("A")}, {Formula("B"), Formula("C")}),
                Sequent({Formula("D"), Formula("E")}, {Formula("F")}),
            ],
            Sequent({Formula("(C)>(D)"), Formula("A"), Formula("E")}, {Formula("B"), Formula("F")}),
            True,
        ),
        # {A} |- {B, C}
        # ----------------------------
        # {C -> D, A, E} |- {B, F}
        (
            [
                Sequent({Formula("A")}, {Formula("B"), Formula("C")}),
            ],
            Sequent({Formula("(C)>(D)"), Formula("A"), Formula("E")}, {Formula("B"), Formula("F")}),
            False,
        ),
    ],
)
def test_Larr(assumption_sequent_list: List[Sequent], conclusion_sequent: Sequent, expected: bool):
    assert is_valid_inference(assumption_sequent_list, conclusion_sequent, "L>") == expected
