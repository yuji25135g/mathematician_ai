from Sequent import Sequent
from typing import List


class Node:
    def __init__(
        self,
        sequent: Sequent,
        inference,
        parent: "Node" | None = None,
        children: List["Node"] = [],
    ) -> None:
        self.sequent = sequent
        self.inference = inference
        self.parent = parent
        self.children = children
