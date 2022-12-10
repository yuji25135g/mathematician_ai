import pytest
from typing import List
from Sequent import Sequent
from Formula import Formula
from inference import is_valid_inference


@pytest.mark.parametrize(
    ("assumption_sequent_list", "conclusion_sequent", "expected"),
    [
        # {A, B} |- {C}
        # -------------
        # {A & B} |- {C}
        (
            [Sequent({Formula("A"), Formula("B")}, {Formula("C")})],
            Sequent({Formula("(A)&(B)")}, {Formula("C")}),
            True,
        ),
        # {A, B} |- {C}
        # -------------
        # {A & B} |- {D}
        (
            [Sequent({Formula("A"), Formula("B")}, {Formula("C")})],
            Sequent({Formula("(A)&(B)")}, {Formula("D")}),
            False,
        ),
        # {A, B} |- {C}
        # -------------
        # {A & !B} |- {C}
        (
            [Sequent({Formula("A"), Formula("B")}, {Formula("C")})],
            Sequent({Formula("(A)&(!(B))")}, {Formula("C")}),
            False,
        ),
    ],
)
def test_Land(assumption_sequent_list: List[Sequent], conclusion_sequent: Sequent, expected: bool):
    assert is_valid_inference(assumption_sequent_list, conclusion_sequent, "L&") == expected
