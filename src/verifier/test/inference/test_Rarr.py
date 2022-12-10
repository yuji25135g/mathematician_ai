import pytest
from typing import List
from Sequent import Sequent
from Formula import Formula
from inference import is_valid_inference


@pytest.mark.parametrize(
    ("assumption_sequent_list", "conclusion_sequent", "expected"),
    [
        # {A, B} |- {C, D}
        # --------------------
        # {B} |- {C, A -> D}
        (
            [
                Sequent({Formula("A"), Formula("B")}, {Formula("C"), Formula("D")}),
            ],
            Sequent({Formula("B")}, {Formula("C"), Formula("(A)>(D)")}),
            True,
        ),
        # {A, B} |- {D}
        # --------------------
        # {B} |- {C, A -> D}
        (
            [
                Sequent({Formula("A"), Formula("B")}, {Formula("D")}),
            ],
            Sequent({Formula("B")}, {Formula("C"), Formula("(A)>(D)")}),
            False,
        ),
    ],
)
def test_Rarr(assumption_sequent_list: List[Sequent], conclusion_sequent: Sequent, expected: bool):
    assert is_valid_inference(assumption_sequent_list, conclusion_sequent, "R>") == expected
