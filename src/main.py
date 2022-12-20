from typing import List, Tuple, TypeAlias, Literal, Dict, Optional, Union
import copy
import os, sys

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from actionGenerator.generateAction import randomAction, generateState, checkLength
from actionGenerator.displaySequent import displaySeq
from verifier.Formula import Formula
from verifier.Sequent import Sequent
from converter.seq2num import seq2num
from reinforcementLearning.Action import Action
from reinforcementLearning.State import State

from collections import defaultdict
import numpy as np
import csv

# 複雑な定理に拡張するとき
# generatedState[0]やstate.state[0]などSequentのListになっているものは修正する


# csvファイルの生成
isFile = os.path.isfile("theorem.csv")
if not isFile:
    with open("theorem.csv", "a") as f:
        writer = csv.writer(f)
        writer.writerow(["theorem", "reward", "proof"])


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
            action: Action = state.actions[
                actionIndex
            ]  # Actionインスタンスを作ってるからgenerateUnActionが使いづらい #generateUnActionもAction型にする?
            if action == "random":
                randAction = randomAction(state.state[0])
                action = Action(randAction[0], randAction[1], randAction[2])
            generateStateArg = state.state + action.list
            generatedState = [generateState(generateStateArg)]

            if generatedState[0] != False:  # 適用できるかチェック
                if checkLength(generatedState[0]):
                    break  # 問題がなければ終了

        # 選ばれたactionが新しかったら先頭に加える
        actionCount = 0
        generatedStateNum = tuple(seq2num(generatedState[0]))
        for i in range(0, len(state.actions) - 1):
            if action.actionNum != state.actions[i].actionNum:
                actionCount += 1
            else:
                print("acttion = " + str(i))
                nextState = state.nextStates[i]
                break
        if actionCount == len(state.actions) - 1:
            if generatedStateNum == state.stateNum:
                nextState = state
            else:
                nextState = State(generatedState, generatedStateNum)
            state.nextStates.insert(0, nextState)
            state.actions.insert(0, action)
            state.q.insert(0, 0)
            state.probs.insert(0, 0)
            actionIndex = 0

        # 選ばれたactionとstateを保存
        proofList.append([state, action])
        proofStrList.append([state.state[0].__str__(), action.list])

        # 報酬設定
        if len(nextState.state) == 1:
            count += 1
            if nextState.reward == None:
                print("---")
                print(nextState.state[0])
                print("Input REWARD")
                reward = int(input())
                nextState.reward = reward
                with open("theorem.csv", "a") as f:
                    writer = csv.writer(f)
                    writer.writerow([nextState.state[0], reward, proofStrList])
            else:
                reward = nextState.reward

        state.update(actionIndex, nextState, reward)
        with open("../" + "visualizer.csv", "a") as f2:
            writer = csv.writer(f2)
            writer.writerow(
                [
                    state.state[0],
                    ",".join((str(n) for n in state.probs[:-1])),
                    "_".join(list(map(lambda x: x.state[0].__str__(), state.nextStates))),
                ]
            )
        print(state.probs)
        print(state.q)
        # doneになってからn回更新したら終了
        if count == 10:
            proofList.append([nextState])
            proofStrList.append([nextState.state[0].__str__()])
            print(proofStrList)
            break
        state = nextState

# %%
