from typing import List

# verifier.FormulaとするとSequent.py単独で実行できなくなる
from verifier.Formula import Formula

MAX_SEQUENT_SIZE = 10


class Sequent:
    def __init__(self, left: set[Formula], right: set[Formula]) -> None:
        self.left = left
        self.right = right

    def __str__(self) -> str:
        left_string = ", ".join(list(map(lambda f: str(f), self.left)))
        right_string = ", ".join(list(map(lambda f: str(f), self.right)))
        return left_string + " |- " + right_string

    def is_axiom(self) -> bool:
        return self.left == self.right

    def is_equal_to(self, other: "Sequent") -> bool:
        return self.left == other.left and self.right == other.right

    def to_real_num_list(self) -> List[float]:
        # 初期化
        left_num_list = [0.0] * MAX_SEQUENT_SIZE
        right_num_list = [0.0] * MAX_SEQUENT_SIZE

        for i, left_formula in enumerate(self.left):
            left_num_list[i] = left_formula.to_real_num()

        for i, right_formula in enumerate(self.right):
            right_num_list[i] = right_formula.to_real_num()

        return left_formula + right_formula
