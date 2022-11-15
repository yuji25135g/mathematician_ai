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
