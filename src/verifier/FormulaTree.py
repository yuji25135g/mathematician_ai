from typing import List, Union, TypeAlias, Literal, Optional, Dict
from Formula import Formula
from collections import deque

Operator: TypeAlias = Literal["!", "&", "|", ">"]

SYMBOL_LIST = ["A", "B", "C", "D", "E", "!", "|", "&", ">"]
NUM_LIST = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]
SYMBOL_NUM_MAP: Dict[str, str] = dict(zip(SYMBOL_LIST, NUM_LIST))


class FormulaTree:
    def __init__(self, tree: List[Union["FormulaTree", str]], operator: Operator = None) -> None:
        self.tree: List[Union["FormulaTree", str]] = tree
        self.operator: Optional[Operator] = operator

    # 論理式の実数変換
    def to_real_num(self) -> float:
        queue = deque([self])
        real_num_str = ""
        # 幅優先探索
        while queue:
            formula_tree = queue.popleft()
            if formula_tree.operator:
                real_num_str += SYMBOL_NUM_MAP[formula_tree.operator]
            for sub_tree in formula_tree.tree:
                if isinstance(sub_tree, str):  # 葉の場合
                    real_num_str += SYMBOL_NUM_MAP[sub_tree]
                else:  # 　内点の場合
                    queue.append(sub_tree)

        return float("0." + real_num_str)

    @classmethod
    def create_from_formula(cls, formula: Formula) -> "FormulaTree":
        # formulaが「X」のとき
        if len(formula.string_formula) == 1:
            return FormulaTree([formula.string_formula])
        # formulaが「!X」のとき
        if formula.string_formula[0] == "!":
            return FormulaTree(
                [
                    FormulaTree.create_from_formula(
                        Formula(formula.string_formula[2 : len(formula.string_formula) - 1])
                    ),
                ],
                "!",
            )
        par_count = 0  # 「(」ひとつにつき+1、 「)」ひとつにつき-1
        operator_idx = 0  # 演算子の位置
        for i in range(len(formula.string_formula)):
            if formula.string_formula[i] == "(":
                par_count += 1
            elif formula.string_formula[i] == ")":
                par_count += -1
            if par_count == 0:
                operator_idx = par_count + 1

        return FormulaTree(
            [
                FormulaTree.create_from_formula(Formula(formula.string_formula[1 : operator_idx - 1])),
                FormulaTree.create_from_formula(
                    Formula(formula.string_formula[operator_idx + 2 : len(formula.string_formula) - 1])
                ),
            ],
            formula.string_formula[operator_idx],
        )
