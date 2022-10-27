from Formula import Formula


class Sequent:
    def __init__(self, left: set[Formula], right: set[Formula]) -> None:
        self.left = left
        self.right = right
