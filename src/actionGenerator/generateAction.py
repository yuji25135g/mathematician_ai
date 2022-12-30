import random
import numpy as np
import copy

import os, sys

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from verifier.Formula import Formula
from verifier.Sequent import Sequent

sequent_maxLen = 8  # シーケントの両辺の論理式の上限
fml_maxLen = 8  # 各論理式に出現する命題変数の総数の上限

AP = ["A", "B", "C"]  # 命題変数のリスト

unInf = ["Emp", "LW", "RW", "L&", "R|", "R>", "L!", "R!"]  # 1引数の推論規則, Empは恒等action
binInf = ["R&", "L|", "L>"]  # 2引数の推論規則


def generateState(ls):  # ls=[推論規則, 親シーケント, 親シーケント, 引数1, 引数2] を受け取って子のシーケントを生成, 適用できない場合はFalseを返す
    left_seq1 = copy.copy(ls[1].left)
    right_seq1 = copy.copy(ls[1].right)
    left_seq2 = copy.copy(ls[2].left)
    right_seq2 = copy.copy(ls[2].right)
    argFml1 = Formula(ls[3])
    argFml2 = Formula(ls[4])

    if ls[0] == "Emp":
        return ls[1]
    elif ls[0] == "LW":
        left_seq1.add(Formula(ls[3]))
        return Sequent(left_seq1, right_seq1)
    elif ls[0] == "RW":
        right_seq1.add(Formula(ls[3]))
        return Sequent(left_seq1, right_seq1)

    elif ls[0] == "L&":
        if (Formula(ls[3]) in left_seq1) & (Formula(ls[4]) in left_seq1):
            conc = "(" + ls[3] + ")&(" + ls[4] + ")"
            left_seq1.add(Formula(conc))
            left_seq1.remove(Formula(ls[3]))
            left_seq1.remove(Formula(ls[4]))
            return Sequent(left_seq1, right_seq1)
        else:
            return False

    elif ls[0] == "R|":
        if (Formula(ls[3]) in right_seq1) & (Formula(ls[4]) in right_seq1):
            conc = "(" + ls[3] + ")|(" + ls[4] + ")"
            right_seq1.add(Formula(conc))
            right_seq1.remove(Formula(ls[3]))
            right_seq1.remove(Formula(ls[4]))
            return Sequent(left_seq1, right_seq1)
        else:
            return False

    elif ls[0] == "R>":
        if (Formula(ls[3]) in left_seq1) & (Formula(ls[4]) in right_seq1):
            conc = "(" + ls[3] + ")>(" + ls[4] + ")"
            right_seq1.add(Formula(conc))
            left_seq1.remove(Formula(ls[3]))
            right_seq1.remove(Formula(ls[4]))
            return Sequent(left_seq1, right_seq1)
        else:
            return False

    elif ls[0] == "L!":
        if Formula(ls[3]) in right_seq1:
            conc = "!(" + ls[3] + ")"
            left_seq1.add(Formula(conc))
            right_seq1.remove(Formula(ls[3]))
            return Sequent(left_seq1, right_seq1)
        else:
            return False

    elif ls[0] == "R!":
        if Formula(ls[3]) in left_seq1:
            conc = "!(" + ls[3] + ")"
            right_seq1.add(Formula(conc))
            left_seq1.remove(Formula(ls[3]))
            return Sequent(left_seq1, right_seq1)
        else:
            return False

    elif ls[0] == "R&":
        if (Formula(ls[3]) in right_seq1) & (Formula(ls[4]) in right_seq2):
            new_right_seq = right_seq1.remove(argFml1)
            if (left_seq1 == left_seq2) & (new_right_seq.add(argFml2) == right_seq2):
                return Sequent(
                    left_seq1,
                    new_right_seq.remove(argFml2).add(
                        Formula("(" + argFml1.string_formula + ")&(" + argFml2.string_formula + ")")
                    ),
                )
        else:
            return False
    elif ls[0] == "L|":
        if (Formula(ls[3]) in left_seq1) & (Formula(ls[4]) in left_seq2):
            new_left_seq = left_seq1.remove(argFml1)
            if (right_seq1 == right_seq2) & (new_left_seq.add(argFml2) == left_seq2):
                return Sequent(
                    new_left_seq.remove(argFml2).add(
                        Formula("(" + argFml1.string_formula + ")|(" + argFml2.string_formula + ")")
                    ),
                    right_seq1,
                )
        else:
            return False
    elif ls[0] == "L>":
        if (Formula(ls[3]) in right_seq1) & (Formula(ls[4]) in left_seq2):
            new_right_seq = right_seq1
            new_right_seq.remove(Formula(ls[3]))
            new_right_seq = new_right_seq | right_seq2
            new_left_seq = left_seq2
            new_left_seq.remove(Formula(ls[4]))
            new_left_seq = new_left_seq | left_seq1
            new_left_seq.add(Formula("(" + argFml1.string_formula + ")>(" + argFml2.string_formula + ")"))
            return Sequent(new_left_seq, new_right_seq)
        else:
            return False


def randomUnAction(state: Sequent):
    soundness = False  # ランダムに選んだ規則を適用できるか？

    actionInf = "Emp"
    argFml1 = ""
    argFml2 = ""

    while soundness == False:
        actionInf = random.choice(unInf)
        if actionInf == "Emp":
            soundness = True
            argFml1 = ""
            argFml2 = ""

        elif actionInf in ["LW", "RW"]:
            soundness = True
            argFml1 = random.choice(AP)
            argFml2 = ""

        elif actionInf == "L&":
            if len(state.left) >= 2:
                soundness = True
                args = random.sample(list(state.left), 2)
                argFml1 = args[0].string_formula
                argFml2 = args[1].string_formula

        elif actionInf == "R|":
            if len(state.right) >= 2:
                soundness = True
                args = random.sample(list(state.right), 2)
                argFml1 = args[0].string_formula
                argFml2 = args[1].string_formula

        elif actionInf == "R>":
            if len(state.left) >= 1 & len(state.right) >= 1:
                soundness = True
                argFml1 = random.choice(list(state.left)).string_formula
                argFml2 = random.choice(list(state.right)).string_formula

        elif actionInf == "L!":
            if len(state.right) >= 1:
                soundness = True
                argFml1 = random.choice(list(state.right)).string_formula

        elif actionInf == "R!":
            if len(state.left) >= 1:
                soundness = True
                argFml1 = random.choice(list(state.left)).string_formula

    return [actionInf, state, state, argFml1, argFml2]


def randomBinAction(seq1, seq2):
    actionInf = "Emp"
    argFml1 = ""
    argFml2 = ""
    soundness = False

    for i in range(10):  # 10回まで挑戦
        left_seq1 = copy.copy(seq1.left)
        right_seq1 = copy.copy(seq1.right)
        left_seq2 = copy.copy(seq2.left)
        right_seq2 = copy.copy(seq2.right)

        actionInf = random.choice(binInf)
        if (actionInf == "R&") & (len(seq1.right) >= 1) & (len(seq2.right) >= 1):
            argFml1 = random.choice(list(right_seq1))
            argFml2 = random.choice(list(right_seq2))
            right_seq1.remove(argFml1)
            right_seq2.remove(argFml2)
            if (seq1.left == seq2.left) & (right_seq1 == right_seq2):
                soundness = True
                break

        elif (actionInf == "L|") & (len(seq1.left) >= 1) & (len(seq2.left) >= 1):
            argFml1 = random.choice(list(left_seq1))
            argFml2 = random.choice(list(left_seq2))
            left_seq1.remove(argFml1)
            left_seq2.remove(argFml2)
            if (seq1.right == seq2.right) & (left_seq1 == left_seq2):
                soundness = True
                break

        elif (actionInf == "L>") & (len(seq1.right) >= 1) & (len(seq2.left) >= 1):
            argFml1 = random.choice(list(right_seq1))
            argFml2 = random.choice(list(left_seq2))
            soundness = True
            break

    if soundness == False:
        return ["Emp", seq1, seq1, "", ""]
    else:
        return [actionInf, seq1, seq2, argFml1.string_formula, argFml2.string_formula]


def checkLength(state):  # 長さの上限チェック
    if len(state.left) + len(state.left) > sequent_maxLen:
        return False
    else:
        for i in list(state.left) + list(state.left):
            ap_num = 0
            for ap in AP:
                ap_num += i.string_formula.count(ap)
            if ap_num > fml_maxLen:
                return False
    return True


def generateAction(state, actionList, actionProbs):

    actionList.append("random_action")  # 末尾のアクションを抽選

    while True:  # 適用できなければやり直す
        Done = False
        seqNumList = [i for i in range(len(state))]  # シーケントのインデックスのリスト
        actionNum = np.random.choice(len(actionList), p=actionProbs)
        action = actionList[actionNum]
        if action == "random_action":  # ランダムなアクションに挑戦する場合
            if len(state) <= 1:
                action = randomUnAction(state[0])
                newSeq = generateState(action)
                if newSeq != False:  # 適用できるかチェック
                    if checkLength(newSeq):  # 長さのチェック
                        next_state = [newSeq]
                        Done = True
                        break  # 問題がなければ終了
            else:
                aryNum = np.random.choice([0, 1], p=[0.3, 0.7])  # 二引数に挑戦する確率
                if aryNum == 0:  # 一引数の場合
                    seqNums = random.sample(seqNumList, 1)  # 適用するシーケントを一つ選択
                    action = randomUnAction(state[seqNums[0]])  # 1引数のアクションをランダム生成
                    newSeq = generateState(action)  # 生成したアクションの適用
                    if newSeq != False:  # 適用できるかチェック
                        if checkLength(newSeq):  # 長さのチェック
                            next_state = copy.copy(state)
                            next_state[seqNums[0]] = newSeq  # シーケントを適用後のものに置き換え
                            break
                else:  # 二引数の場合
                    seqNums = random.sample(seqNumList, 2)  # 適用するシーケントを2つ選択
                    action = randomBinAction(state[seqNums[0]], state[seqNums[1]])  # 2引数のアクションをランダム生成
                    if action[0] != "Emp":  # R&, L|, L->が適用できそうなとき
                        newSeq = generateState(action)  # 生成したアクションの適用
                        if newSeq != False:  # 適用できるかチェック
                            if checkLength(newSeq):  # 長さのチェック
                                next_state = copy.copy(state)
                                next_state.remove(state[seqNums[0]])  # 適用前のシーケントを除去1
                                next_state.remove(state[seqNums[1]])  # 適用前のシーケントを除去2
                                next_state.append(newSeq)  # 適用後のシーケントを追加
                                if len(next_state) == 1:
                                    Done = True
                                break
        else:  # 過去のアクションから選ぶ場合. 以下はほぼ同様
            if (action[1] in state) & (action[2] in state):
                newSeq = generateState(action)
                if (newSeq != False) & (action[0] == "Emp"):  # 適用できるかチェック
                    next_state = copy.copy(state)
                    if len(next_state) == 1:
                        Done = True
                    break
                elif (newSeq != False) & (action[0] in binInf):  # 適用できるかチェック
                    if checkLength(newSeq):  # 長さのチェック
                        next_state = copy.copy(state)
                        next_state.remove(state[seqNums[0]])
                        next_state.remove(state[seqNums[1]])
                        next_state.append(newSeq)
                        if len(next_state) == 1:
                            Done = True
                        break
                elif newSeq != False:
                    if checkLength(newSeq):  # 長さのチェック
                        next_state = copy.copy(state)
                        next_state.remove(state[seqNums[0]])
                        next_state.append(newSeq)
                        if len(next_state) == 1:
                            Done = True
                        break

    return [action, next_state, Done]
