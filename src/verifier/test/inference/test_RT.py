import pytest
from typing import List
from Sequent import Sequent
from Formula import Formula
from inference import is_valid_inference


@pytest.mark.parametrize(
    ("assumption_sequent_list", "conclusion_sequent", "expected"),
    [
        # {A} |- {B}
        # -------------
        # {C} |- {D, 1}
        (
            [Sequent({Formula("A")}, {Formula("B")})],
            Sequent({Formula("C")}, {Formula("D"), Formula("1")}),
            True,
        ),
        # {A} |- {B}
        # -------------
        # {C} |- {D}
        (
            [Sequent({Formula("A")}, {Formula("B")})],
            Sequent({Formula("C")}, {Formula("D")}),
            False,
        ),
    ],
)
def test_RT(
    assumption_sequent_list: List[Sequent], conclusion_sequent: Sequent, expected: bool
):
    assert (
        is_valid_inference(assumption_sequent_list, conclusion_sequent, "RT")
        == expected
    )
