from Formula import Formula


class Sequent:
    def __init__(self, left: set[Formula], right: set[Formula]) -> None:
        self.left = left
        self.right = right

    def is_axiom(self) -> bool:
        return self.left == self.right
