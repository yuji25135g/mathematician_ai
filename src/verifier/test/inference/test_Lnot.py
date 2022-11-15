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
        # {!C, A} |- {B}
        (
            [Sequent({Formula("A")}, {Formula("B"), Formula("C")})],
            Sequent({Formula("!(C)"), Formula("A")}, {Formula("B")}),
            True,
        ),
        # {A} |- {B, C}
        # -------------
        # {!C, D} |- {B}
        (
            [Sequent({Formula("A")}, {Formula("B"), Formula("C")})],
            Sequent({Formula("!(C)"), Formula("D")}, {Formula("B")}),
            False,
        ),
        # {A} |- {B, C}
        # -------------
        # {!C, A} |- {B, D}
        (
            [Sequent({Formula("A")}, {Formula("B"), Formula("C")})],
            Sequent({Formula("!(C)"), Formula("A")}, {Formula("B"), Formula("D")}),
            False,
        ),
    ],
)
def test_Lnot(assumption_sequent_list: List[Sequent], conclusion_sequent: Sequent, expected: bool):
    assert is_valid_inference(assumption_sequent_list, conclusion_sequent, "L!") == expected
