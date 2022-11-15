import pytest
from typing import List
from Sequent import Sequent
from Formula import Formula
from inference import is_valid_inference


@pytest.mark.parametrize(
    ("assumption_sequent_list", "conclusion_sequent", "expected"),
    [
        # {A} |- {C}
        # -------------
        # {A, B} |- {C}
        (
            [Sequent({Formula("A")}, {Formula("C")})],
            Sequent({Formula("A"), Formula("B")}, {Formula("C")}),
            True,
        ),
        # {A} |- {C}
        # -------------
        # {A} |- {C}
        (
            [Sequent({Formula("A")}, {Formula("C")})],
            Sequent({Formula("A")}, {Formula("C")}),
            False,
        ),
    ],
)
def test_LW(assumption_sequent_list: List[Sequent], conclusion_sequent: Sequent, expected: bool):
    assert is_valid_inference(assumption_sequent_list, conclusion_sequent, "LW") == expected
