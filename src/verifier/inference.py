from typing import List, TypeAlias, Literal
from Sequent import Sequent
from Formula import Formula

InferenceStr: TypeAlias = Literal[
    "LW",
    "RW",
    "LC",
    "RC",
    "LX",
    "RX",
    "LF",
    "RT",
    "L&1",
    "L&2",
    "R&",
    "L|",
    "R|1",
    "R|2",
    "L->",
    "R->",
    "L!",
    "R!",
    "AX",
]


def is_valid_inference(
    assumption_sequent_list: List[Sequent],
    conclusion_sequent: Sequent,
    inference: InferenceStr,
) -> bool:
    match inference:
        case "LW":
            if len(assumption_sequent_list) != 1:
                return False
            if (
                conclusion_sequent.left > assumption_sequent_list[0].left
                and len(conclusion_sequent.left - assumption_sequent_list[0].left) == 1
                and assumption_sequent_list[0].right == conclusion_sequent.right
            ):
                return True
            else:
                return False

        case "RW":
            if len(assumption_sequent_list) != 1:
                return False
            if (
                conclusion_sequent.right > assumption_sequent_list[0].right
                and len(conclusion_sequent.right - assumption_sequent_list[0].right) == 1
                and assumption_sequent_list[0].left == conclusion_sequent.left
            ):
                return True
            else:
                return False

        case "LC" | "RC" | "LX" | "RX":
            if len(assumption_sequent_list) != 1:
                return False
            if (
                assumption_sequent_list[0].left == conclusion_sequent.left
                and assumption_sequent_list[0].right == conclusion_sequent.right
            ):
                return True
            else:
                return False

        case "LF":
            if Formula("0") in conclusion_sequent.left:
                return True
            else:
                return False

        case "RT":
            if Formula("1") in conclusion_sequent.right:
                return True
            else:
                return False

        case "L&1" | "L&2":
            if len(assumption_sequent_list) != 1:
                return False
            if assumption_sequent_list[0].right != conclusion_sequent.right:
                return False
            ass_rest = assumption_sequent_list[0].left - (assumption_sequent_list[0].left & conclusion_sequent.left)
            con_rest = conclusion_sequent.left - (assumption_sequent_list[0].left & conclusion_sequent.left)
            if len(ass_rest) != 1 or len(con_rest) != 1:
                return False

            ass_top_nodes, ass_op = list(ass_rest)[0].get_top_terms()
            con_top_nodes, con_op = list(con_rest)[0].get_top_terms()
            if con_op != "&":
                return False

            if ass_op == "&":
                if set(ass_top_nodes) <= set(con_top_nodes):
                    return True
            else:
                if list(ass_rest)[0].string_formula in con_top_nodes:
                    return True
            return False

        case "R&":
            if len(assumption_sequent_list) != 2:
                return False

            if (
                assumption_sequent_list[0].left != conclusion_sequent.left
                or assumption_sequent_list[1].left != conclusion_sequent.left
            ):
                return False

            if len(assumption_sequent_list[0].right) != len(assumption_sequent_list[1].right) or len(
                assumption_sequent_list[0].right
            ) != len(conclusion_sequent.right):
                return False

            ass_intersection = assumption_sequent_list[0].right & assumption_sequent_list[1].right
            ass_rest_1 = assumption_sequent_list[0].right - ass_intersection
            ass_rest_2 = assumption_sequent_list[1].right - ass_intersection
            if len(ass_rest_1) != 1 or len(ass_rest_2) != 1:
                return False

            con_rest = conclusion_sequent.right - ass_intersection
            if len(con_rest) != 1:
                return False
            con_top_nodes, con_op = list(con_rest)[0].get_top_terms()
            if con_op != "&":
                return False

            ass_top_nodes_1, ass_op_1 = list(ass_rest_1)[0].get_top_terms()
            ass_top_nodes_2, ass_op_2 = list(ass_rest_2)[0].get_top_terms()
            if ass_op_1 == "&" and ass_op_2 == "&":
                if (set(ass_top_nodes_1) | set(ass_top_nodes_2)) == set(con_top_nodes):
                    return True
            elif ass_op_1 == "&":
                if (set(ass_top_nodes_1) | {list(ass_rest_2)[0].string_formula}) == set(con_top_nodes):
                    return True
            elif ass_op_2 == "&":
                if (set(ass_top_nodes_2) | {list(ass_rest_1)[0].string_formula}) == set(con_top_nodes):
                    return True
            else:
                if {
                    list(ass_rest_1)[0].string_formula,
                    list(ass_rest_2)[0].string_formula,
                } == set(con_top_nodes):
                    return True
            return False

        case "L|":
            if len(assumption_sequent_list) != 2:
                return False

            if (
                assumption_sequent_list[0].right != conclusion_sequent.right
                or assumption_sequent_list[1].right != conclusion_sequent.right
            ):
                return False

            if len(assumption_sequent_list[0].left) != len(assumption_sequent_list[1].left) or len(
                assumption_sequent_list[0].left
            ) != len(conclusion_sequent.left):
                return False

            ass_intersection = assumption_sequent_list[0].left & assumption_sequent_list[1].left
            ass_rest_1 = assumption_sequent_list[0].left - ass_intersection
            ass_rest_2 = assumption_sequent_list[1].left - ass_intersection
            if len(ass_rest_1) != 1 or len(ass_rest_2) != 1:
                return False

            con_rest = conclusion_sequent.left - ass_intersection
            if len(con_rest) != 1:
                return False
            con_top_nodes, con_op = list(con_rest)[0].get_top_terms()
            if con_op != "|":
                return False

            ass_top_nodes_1, ass_op_1 = list(ass_rest_1)[0].get_top_terms()
            ass_top_nodes_2, ass_op_2 = list(ass_rest_2)[0].get_top_terms()
            if ass_op_1 == "|" and ass_op_2 == "|":
                if (set(ass_top_nodes_1) | set(ass_top_nodes_2)) == set(con_top_nodes):
                    return True
            elif ass_op_1 == "|":
                if (set(ass_top_nodes_1) | {list(ass_rest_2)[0].string_formula}) == set(con_top_nodes):
                    return True
            elif ass_op_2 == "|":
                if (set(ass_top_nodes_2) | {list(ass_rest_1)[0].string_formula}) == set(con_top_nodes):
                    return True
            else:
                if {
                    list(ass_rest_1)[0].string_formula,
                    list(ass_rest_2)[0].string_formula,
                } == set(con_top_nodes):
                    return True
            return False

        case "R|1" | "R|2":
            if len(assumption_sequent_list) != 1:
                return False

            if assumption_sequent_list[0].left != conclusion_sequent.left:
                return False

            ass_rest = assumption_sequent_list[0].right - (assumption_sequent_list[0].right & conclusion_sequent.right)
            con_rest = conclusion_sequent.right - (assumption_sequent_list[0].right & conclusion_sequent.right)
            if len(ass_rest) != 1 or len(con_rest) != 1:
                return False

            ass_top_nodes, ass_op = list(ass_rest)[0].get_top_terms()
            con_top_nodes, con_op = list(con_rest)[0].get_top_terms()
            if con_op != "|":
                return False

            if ass_op == "&":
                if set(ass_top_nodes) <= set(con_top_nodes):
                    return True
            else:
                if list(ass_rest)[0].string_formula in con_top_nodes:
                    return True
            return False

        case "L!":
            if len(assumption_sequent_list) != 1:
                return False
            if (
                assumption_sequent_list[0].right <= conclusion_sequent.right
                or len(assumption_sequent_list[0].right) != len(conclusion_sequent.right) + 1
            ):
                return False

            if (
                assumption_sequent_list[0].left >= conclusion_sequent.left
                or len(assumption_sequent_list[0].left) != len(conclusion_sequent.left) - 1
            ):
                return False

            ass_right_rest = assumption_sequent_list[0].right - (
                assumption_sequent_list[0].right & conclusion_sequent.right
            )
            con_left_rest = conclusion_sequent.left - (conclusion_sequent.left & assumption_sequent_list[0].left)

            if len(ass_right_rest) != 1 or len(con_left_rest) != 1:
                return False

            if f"!({list(ass_right_rest)[0].string_formula})" == list(con_left_rest)[0].string_formula:
                return True
            else:
                return False

        case "R!":
            if len(assumption_sequent_list) != 1:
                return False
            if (
                assumption_sequent_list[0].left <= conclusion_sequent.left
                or len(assumption_sequent_list[0].left) != len(conclusion_sequent.left) + 1
            ):
                return False

            if (
                assumption_sequent_list[0].right >= conclusion_sequent.right
                or len(assumption_sequent_list[0].right) != len(conclusion_sequent.right) - 1
            ):
                return False

            ass_left_rest = assumption_sequent_list[0].left - (
                assumption_sequent_list[0].left & conclusion_sequent.left
            )
            con_right_rest = conclusion_sequent.right - (conclusion_sequent.right & assumption_sequent_list[0].right)

            if len(ass_left_rest) != 1 or len(con_right_rest) != 1:
                return False

            if f"!({list(ass_left_rest)[0].string_formula})" == list(con_right_rest)[0].string_formula:
                return True
            else:
                return False

        case _:
            raise ValueError(f"inference {inference} is not exit")
