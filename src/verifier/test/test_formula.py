import pytest
from Formula import Formula
from typing import List, Tuple


@pytest.mark.parametrize(
    ("formula1", "formula2", "expected"),
    [
        # ふたつの論理式文字列が等しい
        (Formula("(A)"), Formula("(A)"), True),
        # ふたつの論理式文字列が等しくない
        (Formula("(A)"), Formula("(B)"), False),
    ],
)
def test_eq(formula1, formula2, expected):
    assert (formula1 == formula2) == expected


@pytest.mark.parametrize(
    ("formula", "result"),
    [
        # 項がひとつのときは、演算子なし
        (Formula("(A)"), (["A"], "")),
        # 項がひとつのときは、演算子なし
        (Formula("(!(A))"), (["!(A)"], "")),
        # 項がふたつで演算子が　and
        (Formula("(A)&(!(B))"), (["A", "!(B)"], "&")),
        # 項がふたつで演算子が　or
        (Formula("(!(A))|(B)"), (["!(A)", "B"], "|")),
        # topの項はひとつで前にnotがつく
        (Formula("!((A)&((!(B))|(C)))"), (["(A)&((!(B))|(C))"], "!")),
        # 複雑な論理式
        (
            Formula("(A)|((!(B))|(C))|(!((!(C))&(D)))"),
            (["A", "(!(B))|(C)", "!((!(C))&(D))"], "|"),
        ),
        # 演算子が 「>」
        (Formula("(A)>(B)"), (["A", "B"], ">")),
    ],
)
def test_get_top_terms(formula: Formula, result: Tuple[List[str], str]):
    assert formula.get_top_terms() == result


@pytest.mark.parametrize(("formula", "result"), [(Formula("((A)>(!(B)))&((C)|(D))"), "(A -> (!B)) & (C | D)")])
def test_to_str(formula: Formula, result: str):
    assert str(formula) == result
