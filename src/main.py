from typing import List, Tuple, TypeAlias, Literal, Dict, Optional, Union
import os, sys

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from actionGenerator.generateAction import generateUnAction
from actionGenerator.displaySequent import displaySeq
from verifier.Formula import Formula
from verifier.Sequent import Sequent

seq1 = Sequent({Formula("C"), Formula("B")}, {Formula("!(A)")})

print(displaySeq(seq1))

result = generateUnAction(seq1, [["L!", "!(B)", ""], ["R!", "A", ""]], [0.2, 0.3, 0.5])
print(result[1])
print(displaySeq(result[0]))


from collections import defaultdict
import numpy as np

InferenceStr: TypeAlias = Literal[
    "LW",
    "RW",
    "LC",
    "RC",
    "LX",
    "RX",
    "LF",
    "RT",
    "L&",
    "R&",
    "L|",
    "R|",
    "L>",
    "R>",
    "L!",
    "R!",
    "AX",
]


# 綺麗な型定義ができない...

class Action:
    def __init__(self, inference: InferenceStr, formula1: Optional[Formula] = None, formula2: Optional[Formula] = None):
        self.inference = inference
        self.formula1 = formula1
        self.formula2 = formula2
class State:
    def __init__(self, sequentList: List[Sequent], actionList: List[Union[Action, Literal['random']]] = [], probsList: List[float] = [], nextStateDict: Dict[str, "State"] = {}):
        self.currentState = sequentList
        self.actions = actionList
        self.probs = probsList
        self.nextStates = nextStateDict

#%%
episodes = 10000
for episode in range(episodes):
    state = initialState
    while True:
        while True:
            action = np.random.choice(state.actions, p=state.probs)
            if action == 'random':
                action = randomAction
            nextState = generateState([state] + action)
            if nextState != False:  # 適用できるかチェック
                if checkLength(nextState):  # 長さのチェック
                    break  # 問題がなければ終了
        agent.update(state, action, reward, nextState, done)
        if done:

env.render_q(agent.Q)
