from verifier.Formula import Formula

maxSeqSize = 10
# シーケントの片辺の論理式の数の上限

""" #変数の名前替え. 後回し.
def sortNum(seqNums):
    numlist=[]
    APnum=[5,6,7,8,9]
    for fml in seqNums:
        for n in fml:
            if (n in AP) & (n not in numlist):
                numlist.append(n)
    for i in len(seqNums):
        seqNums[i]=seqNums[i].replace()
"""


def seq2num(seq):
    leftFmlNums = [0] * maxSeqSize
    rightFmlNums = [0] * maxSeqSize
    for i in range(len(list(seq.left))):
        fml = Formula(list(seq.left)[i].string_formula)
        leftFmlNums[i] = fml.to_real_num()
    for i in range(len(list(seq.right))):
        fml = Formula(list(seq.right)[i].string_formula)
        rightFmlNums[i] = fml.to_real_num()
    return tuple(leftFmlNums + rightFmlNums)


# 以下実行例 理解したら消してください

# seq1=Sequent({Formula("A"),Formula("B")},{Formula("!(A)"),Formula("(A)|(B)"),Formula("!((A)&(!(B)))")})
# print(displaySequent.displaySeq(seq1))
# print(seq2num(seq1))
