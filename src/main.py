from typing import List, Tuple, TypeAlias, Literal, Dict, Optional, Union
import copy
import os, sys

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from actionGenerator.generateAction import randomAction, generateState, checkLength
from actionGenerator.displaySequent import displaySeq
from verifier.Formula import Formula
from verifier.Sequent import Sequent
from converter.fml2num import fml2num
from converter.seq2num import seq2num

from collections import defaultdict
import numpy as np

# R->とR>揃えよう　参照：generateAction
InferenceStr: TypeAlias = Literal[
    "LW", "RW", "LC", "RC", "LX", "RX", "LF", "RT", "L&", "R&", "L|", "R|", "L>", "R>", "L!", "R!", "AX", "Emp"
]

inferenceTuple: Tuple[str] = (
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
    "R->",
    "L!",
    "R!",
    "AX",
    "Emp",
)


class Action:
    def __init__(self, inference: InferenceStr, formula1: Optional[str] = None, formula2: Optional[str] = None):
        self.inference = inference
        self.formula1 = formula1
        self.formula2 = formula2
        self.list = [inference, formula1, formula2]
        infIndex = inferenceTuple.index(inference)
        if formula1 == "":
            numFml1 = 0
        else:
            numFml1 = fml2num(self.formula1)
        if formula2 == "":
            numFml2 = 0
        else:
            numFml2 = fml2num(self.formula2)
        self.actionNum = (infIndex, numFml1, numFml2)


class State:
    def __init__(
        self,
        sequentList: Tuple[Sequent],
        stateNum: Tuple[float],
        actionList: List[Union[Action, Literal["random"]]] = ["random"],
        probsList: List[float] = [1.0],
        nextStateDict: Dict[Tuple[float], "State"] = {},
        q: List[float] = [0],
    ):
        self.gamma = 0.9
        self.alpha = 0.8
        self.epsilon = 0.9

        self.state = sequentList
        self.stateNum = stateNum

        # なぜか引数から初期化すると、クラス変数になる
        self.actions: List[Union[Action, Literal["random"]]] = ["random"]  # randomもactionに入れていいのか。->良い
        self.probs: List[float] = [1.0]
        self.q: List[float] = [0]

        self.nextStates: Dict[Tuple[float], "State"] = {}

    def update(
        self,
        actionIndex: int,
        nextState: "State",
        reward: int = 0,
    ):
        next_qs = nextState.q
        next_q_max = max(next_qs)

        target = reward + self.gamma * next_q_max
        self.q[actionIndex] += (target - self.q[actionIndex]) * self.alpha

        self.probs = greedy_probs(self.q, self.epsilon)


def greedy_probs(q: List[float], epsilon: float = 0):
    actionSize = len(q)
    max_action = np.argmax(q)

    base_prob = epsilon / actionSize
    action_probs = [base_prob for i in range(actionSize)]
    action_probs[max_action] += 1 - epsilon
    return action_probs


episodes = 1
initialState = State([Sequent({Formula("A")}, {Formula("A")})], seq2num(Sequent({Formula("A")}, {Formula("A")})))
for episode in range(episodes):
    state: State = initialState
    count: int = 0
    proofList = []
    proofStrList = []

    while True:
        # 適切なActionとNextStateを決定する
        while True:
            actionIndex: int = np.random.choice(np.arange(len(state.actions)), p=state.probs)
            action: Action = state.actions[actionIndex]
            if action == "random":
                randAction = randomAction(state.state[0])
                action = Action(randAction[0], randAction[1], randAction[2])  # 1,2がFormula型ではなく、str
            generateStateArg = state.state + action.list
            generatedState = [generateState(generateStateArg)]
            generatedStateNum = tuple(seq2num(generatedState[0]))  # 一本道じゃなくなったら破綻する

            # 生成したStateからnextStateを作る
            if generatedStateNum in state.nextStates.keys():
                nextState = state.nextStates[generatedStateNum]
            elif generatedStateNum == state.stateNum:
                nextState = state
            else:
                nextState = State(generatedState, generatedStateNum)
                state.nextStates[generatedStateNum] = nextState

            if nextState != False:  # 適用できるかチェック
                if checkLength(nextState.state[0]):  # 長さのチェック.ここも一本道じゃなくなったら破綻
                    break  # 問題がなければ終了

        # 選ばれたactionが新しかったら先頭に加える
        actionCount = 0
        for i in range(0, len(state.actions) - 1):
            if action.actionNum != state.actions[i].actionNum:
                actionCount += 1
        if actionCount == len(state.actions) - 1:
            state.actions.insert(0, action)
            state.q.insert(0, 0)
            state.probs.insert(0, 0)
            actionIndex = 0

        # 選ばれたactionとstateを保存
        proofList.append([state, action])
        proofStrList.append([state.state[0].__str__(), action.list])  # ここも一本道じゃなくなったら破綻

        if len(nextState.state) == 1:
            count += 1
            print("---")
            print(nextState.state[0])
            print("Input REWARD")
            reward = int(input())
        state.update(actionIndex, nextState, reward)
        print(state.probs)
        print(state.q)
        # doneになってから10回更新したら終了
        if count == 2:
            proofList.append([nextState])
            proofStrList.append([nextState.state[0].__str__()])
            print(proofStrList)
            break
        state = nextState

# %%
