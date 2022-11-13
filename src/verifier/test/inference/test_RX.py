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
        # {A} |- {C, B}
        (
            [Sequent({Formula("A")}, {Formula("B"), Formula("C")})],
            Sequent({Formula("A")}, {Formula("C"), Formula("B")}),
            True,
        ),
        # {A, B} |- {C}
        # -------------
        # {A} |- {C}
        (
            [Sequent({Formula("A"), Formula("B")}, {Formula("C")})],
            Sequent({Formula("A")}, {Formula("C")}),
            False,
        ),
    ],
)
def test_LX(
    assumption_sequent_list: List[Sequent], conclusion_sequent: Sequent, expected: bool
):
    assert (
        is_valid_inference(assumption_sequent_list, conclusion_sequent, "LX")
        == expected
    )
