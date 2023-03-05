import re

#パス直書きしてるのよくない。
#問題のとこでパスを完成させる
def GetBaseDataPath(aCourse:str,aPart:str) -> str:
    tBaseDataPath = "../data/"
    tSG = re.findall('SG[0-9][0-9]',aCourse)
    tBaseDataPath += f"{tSG[0]}p{aPart}"
    return tBaseDataPath