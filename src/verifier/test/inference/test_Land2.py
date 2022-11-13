import pytest
from typing import List
from Sequent import Sequent
from Formula import Formula
from inference import is_valid_inference


@pytest.mark.parametrize(
    ("assumption_sequent_list", "conclusion_sequent", "expected"),
    [
        # {D, B} |- {C}
        # -------------
        # {A & D, B} |- {C}
        (
            [Sequent({Formula("D"), Formula("B")}, {Formula("C")})],
            Sequent({Formula("(A)&(D)"), Formula("B")}, {Formula("C")}),
            True,
        ),
        # {D, B} |- {C}
        # -------------
        # {A & D, B} |- {D}
        (
            [Sequent({Formula("D"), Formula("B")}, {Formula("C")})],
            Sequent({Formula("(A)&(D)"), Formula("B")}, {Formula("D")}),
            False,
        ),
        # {D, B} |- {C}
        # -------------
        # {A & D, !B} |- {C}
        (
            [Sequent({Formula("D"), Formula("B")}, {Formula("C")})],
            Sequent({Formula("(A)&(D)"), Formula("!(B)")}, {Formula("C")}),
            False,
        ),
    ],
)
def test_Land2(
    assumption_sequent_list: List[Sequent], conclusion_sequent: Sequent, expected: bool
):
    assert (
        is_valid_inference(assumption_sequent_list, conclusion_sequent, "L&2")
        == expected
    )
