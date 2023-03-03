import pandas as pd
import os
import re

#パス直書きしてるのよくない。
#問題のとこでパスを完成させる
def GetBaseDataPath(aCourse,aPart):
    tBaseDataPath = "../data/"
    tSG = re.findall('SG[0-9][0-9]',aCourse)
    tBaseDataPath += f"{tSG[0]}p{aPart}"
    return tBaseDataPath

def FileEnJpIfNotExistCreate(aPath):
    if not os.path.isfile(aPath):   
        with open(aPath, "w") as f:   # ファイルを作成
            f.write('english,japanese\n')#直書きしてるのよくない
    return

#空白の要素や英語、日本語以外のカラム削除、重複データ削除
def DataEnJpOrganization(aPath): 
    tData = pd.read_csv(aPath, sep=",", encoding='utf_8')
    tData = tData.loc[:,["english","japanese"]]#直書きしてるのよくない
    tData = tData.dropna(how='any',axis=0)
    tData = tData.drop_duplicates(subset="english",keep=False)#直書きしてるのよくない
    tData = tData.drop_duplicates(subset="japanese",keep=False)#直書きしてるのよくない
    tData.to_csv(aPath, sep=",", index = False, encoding='utf_8')
    return

def FileLiIfNotExistCreate(aPath):
    if not os.path.isfile(aPath):  
        with open(aPath, "w") as f:   # ファイルを作成
            f.write('one,two,ans\n')#直書きしてるのよくない
    return

#空白の要素や英語、日本語以外のカラム削除、重複データ削除
def DataLiOrganization(aPath): 
    tData = pd.read_csv(aPath, sep=",", encoding='utf_8')
    tData = tData.loc[:,["one","two","ans"]]#直書きしてるのよくない
    tData = tData.dropna(how='any',axis=0)
    tData = tData.drop_duplicates(subset="one",keep=False)#直書きしてるのよくない
    tData = tData.drop_duplicates(subset="two",keep=False)#直書きしてるのよくない
    tData = tData.drop_duplicates(subset="ans",keep=False)#直書きしてるのよくない
    tData.to_csv(aPath, sep=",", index = False, encoding='utf_8')
    return
