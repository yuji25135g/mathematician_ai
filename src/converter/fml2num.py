AP =["A","B","C","D","E"] #命題変数の一覧
Sym=["!","|","&","->"]+AP #終端記号の一覧

SymNum=['1','2','3','4','5','6','7','8','9'] #対応する実数

def parse(fml): #構文解析
    if len(fml)==1: #命題変数のとき
        return([fml])
    else:
        if fml[0]=="!": #「!X」のとき
            return(["!",parse(fml[2:len(fml)-1])])
        else:
            par=0
            for i in range(len(fml)):
                if fml[i]=="(":
                    par += 1
                elif fml[i]==")":
                    par += -1
                if par==0:
                    if fml[i+1]=='-': #「X->X」のとき
                        return([fml[i+1:i+3],parse(fml[1:i]),parse(fml[i+4:len(fml)-1])])
                    else: #「X&X」,「X|X」のとき
                        return([fml[i+1],parse(fml[1:i]),parse(fml[i+3:len(fml)-1])])
                    break

def bfs(*args): #幅優先探索
    root_str="" #深さ0にある葉頂点を並べた文字列
    child_list=[] #深さ0にある部分木を並べたリスト
    for tree in args:
        if tree in Sym: #その頂点が葉頂点のとき
            root_str+=tree
        else: #その頂点が葉頂点でないとき
            child_list+=tree
    if child_list==[]: #最も深い場合
        return(root_str)
    else: #より深くへ探索する場合
        return(root_str+bfs(*child_list)) #再帰呼び出し

def num_Map(fml): #文字の置き換え　Sym[i] => SymNum[i]
    for i in range(len(Sym)):
        fml=fml.replace(Sym[i],SymNum[i])
    return(fml)

def fml2num(fml):
    num_fml='0.'+num_Map(bfs(*parse(fml)))
    return(float(num_fml))


#print('--------------------------------------')
#txt=input("論理式 : ")
#print('--------------------------------------')
#print("構文解析 : ")
#print(parse(txt))
#print('--------------------------------------')
#print("頂点の列 : " +bfs(*parse(txt)))
#print("対応する実数 : "+ str(fml2num(txt)))
#print('--------------------------------------')
