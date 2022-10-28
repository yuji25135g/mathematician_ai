from typing import List, Tuple


class Formula:
    def __init__(self, string_formula: str) -> None:
        # e.g. "(A) | ((!B) & (C)) | ((0) & (1))"
        if Formula.validate(string_formula):
            self.string_formula = Formula.format(string_formula)
        else:
            raise ValueError(f"{string_formula} is invalid")

    def __eq__(self, other: "Formula") -> bool:
        return self.string_formula == other.string_formula

    def get_top_terms(self) -> Tuple[List[str], str]:
        res = []
        tmp_idx = 0
        s_num = 0
        e_num = 0
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
        return res, operator_str[0]

    @staticmethod
    def validate(string: str) -> bool:
        # TODO: validate with regexp
        return True

    def format(string: str) -> str:
        # TODO: format for equality comparison
        return string
