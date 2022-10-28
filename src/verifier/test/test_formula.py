import pytest
from Formula import Formula


@pytest.mark.parametrize(
    ("formula1", "formula2", "expected"),
    [(Formula("(A)"), Formula("(A)"), True), (Formula("(A)"), Formula("(B)"), False)],
)
def test_eq(formula1, formula2, expected):
    assert (formula1 == formula2) == expected
