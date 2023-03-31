import os, sys

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from actionGenerator.generateAction import generateAction
from verifier.Formula import Formula
from verifier.Sequent import Sequent
from converter.seq2num import seq2num
from reinforcementLearning.Action import Action
from reinforcementLearning.State import State

import numpy as np
import csv

# csvファイルの生成
isFile = os.path.isfile("theorem.csv")
if not isFile:
    with open("theorem.csv", "a") as f:
        writer = csv.writer(f)
        writer.writerow(["theorem", "reward", "proof"])

# データベースの代用
allStates = {}
allStatesLen = 0


episodes = 10  # 探索回数
depth = 3  # 証明木の深さ
initialStateNum = (seq2num(Sequent({Formula("A")}, {Formula("A")})), seq2num(Sequent({Formula("B")}, {Formula("B")})))
initialState = State(
    [Sequent({Formula("A")}, {Formula("A")}), Sequent({Formula("B")}, {Formula("B")})],
    initialStateNum,
)

allStates[initialStateNum] = initialState
allStatesLen += 1

for episode in range(episodes):
    state: State = initialState
    count: int = 0
    proofList = []
    proofStrList = []

    while True:
        actionList = []
        for i in range(len(state.actions) - 1):
            actionList.append(state.actions[i].list)
        action, generatedState, done = generateAction(state.state, actionList, state.probs)
        action = Action(action[0], action[1], action[2], action[3], action[4])

        # Stateの数値変換
        generatedStateNum = []
        for i in range(len(generatedState)):
            generatedStateNum.append(seq2num(generatedState[i]))
        generatedStateNum = tuple(generatedStateNum)

        # 選ばれたstateが新しかったら先頭に加える
        stateCount = 0
        for stateNum in allStates.keys():
            if generatedStateNum == stateNum:  # データベースに存在する
                nextStateCount = 0
                for i in range(0, len(state.nextStates)):
                    if generatedStateNum != state.nextStates[i].stateNum:
                        nextStateCount += 1
                    else:  # nextStateに存在する
                        nextState = state.nextStates[i]
                        actionIndex = i
                        action = state.actions[i]
                        break
                if nextStateCount == len(state.nextStates):  # nextStateに存在しない
                    if generatedStateNum == state.stateNum:  # 自己回帰パターン
                        nextState = state
                    else:  # 別Stateから生成されたパターン
                        nextState = allStates[stateNum]
                    state.nextStates.insert(0, nextState)
                    state.actions.insert(0, action)
                    state.q.insert(0, 0)
                    state.probs.insert(0, 0)
                    actionIndex = 0
                break
            else:
                stateCount += 1

        if stateCount == allStatesLen:  # データベースに存在しない
            nextState = State(generatedState, generatedStateNum)
            allStates[generatedStateNum] = nextState
            state.nextStates.insert(0, nextState)
            state.actions.insert(0, action)
            state.q.insert(0, 0)
            state.probs.insert(0, 0)
            actionIndex = 0
            allStatesLen += 1

        # 選ばれたactionとstateを保存
        proofList.append([state, action])
        proofStrList.append([state.stateStr, action.list])

        # 報酬設定
        reward = 0
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
                    writer.writerow([nextState.stateStr, reward, proofStrList])
            else:
                reward = nextState.reward

        state.update(actionIndex, nextState, reward)
        with open("../" + "visualizer.csv", "a") as f2:
            writer = csv.writer(f2)
            writer.writerow(
                [
                    " $ ".join(list(map(str, state.stateStr))),
                    ",".join((str(n) for n in state.probs[:-1])),
                    "_".join(list(map(lambda x: " $ ".join(map(str, x.stateStr)), state.nextStates))),
                ]
            )
        print(state.probs)
        print(state.q)
        if count == depth:
            proofList.append([nextState])
            proofStrList.append([nextState.stateStr])
            print(proofStrList)
            break
        state = nextState
