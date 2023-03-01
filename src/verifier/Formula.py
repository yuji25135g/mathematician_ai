from typing import List, Tuple
import re
from FormulaTree import FormulaTree


class Formula:
    def __init__(self, string_formula: str) -> None:
        if Formula.validate(string_formula):
            self.string_formula = Formula.format(string_formula)
        else:
            raise ValueError(f"{string_formula} is invalid")

    def __eq__(self, other: "Formula") -> bool:
        return self.string_formula == other.string_formula

    def __str__(self) -> str:
        str = self.string_formula.replace(">", " -> ").replace("&", " & ").replace("|", " | ")
        return re.sub(r"\(([A-Z]+)\)", r"\1", str)

    def __hash__(self) -> int:
        return hash(self.string_formula)

    def to_real_num(self) -> float:
        return FormulaTree.create_from_string(self.string_formula).to_real_num()

    # TODO: FormulaTreeに移行
    def get_top_terms(self) -> Tuple[List[str], str]:
        if self.string_formula[0] == "!":
            return [self.string_formula[2 : len(self.string_formula) - 1]], "!"
        res, tmp_idx, s_num, e_num = [], 0, 0, 0
        for i, s in enumerate(self.string_formula):
            if s == "(":
                s_num += 1
                if s_num == e_num + 1:
                    tmp_idx = i
            elif s == ")":
                e_num += 1
                if s_num == e_num:
                    res.append(self.string_formula[tmp_idx + 1 : i])

        operator_str = self.string_formula
        for s in res:
            operator_str = operator_str.replace(s, "")
        operator_str = operator_str.replace("()", "")
        operator = "" if operator_str == "" else operator_str[0]
        return res, operator

    @staticmethod
    def validate(string: str) -> bool:
        # TODO: validate with regexp
        return True

    def format(string: str) -> str:
        # TODO: format for equality comparison
        return string
