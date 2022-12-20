from typing import List, Tuple, TypeAlias, Literal, Dict, Optional, Union
from verifier.Sequent import Sequent
from reinforcementLearning.Action import Action
import numpy as np


class State:
    def __init__(
        self,
        sequentList: Tuple[Sequent],
        stateNum: Tuple[float],
    ):
        self.gamma = 0.9
        self.alpha = 0.8
        self.epsilon = 0.9

        self.state = sequentList
        self.stateNum = stateNum

        self.actions: List[Union[Action, Literal["random"]]] = ["random"]
        self.probs: List[float] = [1.0]
        self.q: List[float] = [0]

        self.nextStates: List["State"] = []
        self.reward: Optional[float] = None

    def update(
        self,
        actionIndex: int,
        nextState: "State",
        reward: float = 0,
    ):
        next_qs = nextState.q
        next_q_max = max(next_qs)

        target = reward + self.gamma * next_q_max
        self.q[actionIndex] += (target - self.q[actionIndex]) * self.alpha

        self.probs = self.greedy_probs()

    def greedy_probs(self):
        actionSize = len(self.q)
        max_action = np.argmax(self.q)

        base_prob = self.epsilon / actionSize
        action_probs = [base_prob for i in range(actionSize)]
        action_probs[max_action] += 1 - self.epsilon
        return action_probs
