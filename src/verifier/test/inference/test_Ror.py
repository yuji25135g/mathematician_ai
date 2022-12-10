import pytest
from typing import List
from Sequent import Sequent
from Formula import Formula
from inference import is_valid_inference


@pytest.mark.parametrize(
    ("assumption_sequent_list", "conclusion_sequent", "expected"),
    [
        # {A} |- {B, C}
        # -------------
        # {A} |- {B | C}
        (
            [Sequent({Formula("A")}, {Formula("B"), Formula("C")})],
            Sequent({Formula("A")}, {Formula("(B)|(C)")}),
            True,
        ),
        # {A} |- {B, C, D}
        # -------------
        # {A} |- {B, C | D}
        (
            [Sequent({Formula("A")}, {Formula("B"), Formula("C"), Formula("D")})],
            Sequent({Formula("A")}, {Formula("B"), Formula("(C)|(D)")}),
            True,
        ),
        # {A} |- {B, C}
        # -------------
        # {D} |- {B | C}
        (
            [Sequent({Formula("A")}, {Formula("B"), Formula("C")})],
            Sequent({Formula("D")}, {Formula("(B)|(C)")}),
            False,
        ),
    ],
)
def test_Ror(assumption_sequent_list: List[Sequent], conclusion_sequent: Sequent, expected: bool):
    assert is_valid_inference(assumption_sequent_list, conclusion_sequent, "R|") == expected
