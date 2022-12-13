from Formula import Formula


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

    def is_equal_to(self, other: "Sequent"):
        return self.left == other.left and self.right == other.right
