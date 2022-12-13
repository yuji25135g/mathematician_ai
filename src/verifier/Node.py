from Sequent import Sequent
from typing import List
from inference import is_valid_inference, InferenceStr


class Node:
    def __init__(
        self,
        sequent: Sequent,
        inference: InferenceStr = "AX",
        children: List["Node"] = [],
    ) -> None:
        self.sequent = sequent
        self.inference = inference
        self.children = children

    def __str__(self) -> str:
        inference_line_length = (
            sum(map(lambda n: len(str(n.sequent)), self.children)) + 5 * len(self.children)
            if len(self.children) > 0
            else len(str(self.sequent))
        )
        inference_line = "-" * inference_line_length + f" ({self.inference})\n"
        return inference_line + str(self.sequent)

    def get_children_sequent_list(self) -> List[Sequent]:
        return list(map(lambda s: s.sequent, self.children))

    # verify in the case that self is a root of subtree
    def verify_subtree(self) -> bool:
        # if self is a leaf
        if len(self.children) == 0:
            if self.inference == "LF" or self.inference == "RT":
                return is_valid_inference([], self.sequent, self.inference)
            return self.sequent.is_axiom()
        # if self is a not leaf
        else:
            # DFS
            if is_valid_inference(self.get_children_sequent_list(), self.sequent, self.inference):
                for child_node in self.children:
                    return child_node.verify_subtree()
            else:
                print(self.inference)
                return False
