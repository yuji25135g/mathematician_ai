import pytest
from Sequent import Sequent
from Formula import Formula


@pytest.mark.parametrize(
    ("sequent", "expected"),
    [
        # A |- A
        (Sequent({Formula("A")}, {Formula("A")}), True),
        # A |- B
        (Sequent({Formula("A")}, {Formula("B")}), False),
    ],
)
def test_is_axiom(sequent: Sequent, expected: bool):
    assert sequent.is_axiom() == expected


@pytest.mark.parametrize(
    ("sequent1", "sequent2", "expected"),
    [
        (
            Sequent({Formula("A")}, {Formula("A")}),
            Sequent({Formula("A")}, {Formula("A")}),
            True,
        ),
        (
            Sequent({Formula("A")}, {Formula("A")}),
            Sequent({Formula("A")}, {Formula("B")}),
            False,
        ),
    ],
)
def test_is_equal_to(sequent1: Sequent, sequent2: Sequent, expected: bool):
    assert sequent1.is_equal_to(sequent2) == expected
