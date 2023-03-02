import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.expected_conditions import presence_of_element_located
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import os
import argparse
import time
import re
import os
import datetime


#パス直書きしてるのよくない。
#問題のとこでパスを完成させる
def GetBaseDataPath(aCourse,aPart):
    tBaseDataPath = "../data/"
    tSG = re.findall('SG[0-9][0-9]',aCourse)
    tBaseDataPath += f"{tSG[0]}p{aPart}"
    return tBaseDataPath

def FileEnJpIfNotExistCreate(aPath):
    if not os.path.isfile(aPath):   # notを付与することで、Falseの場合に実行（真(True)でない）
        with open(aPath, "w") as f:   # ファイルを作成
            f.write('english,japanese\n')
    return

#空白の要素や英語、日本語以外のカラム削除
def DataEnJpOrganization(aPath): 
    tData = pd.read_csv(aPath, sep=",", encoding='utf_8')
    tData = tData.loc[:,["english","japanese"]]
    tData = tData.dropna(how='any',axis=0)
    tData = tData.drop_duplicates(subset="english",keep=False)
    tData = tData.drop_duplicates(subset="japanese",keep=False)
    tData.to_csv(aPath, sep=",", index = False, encoding='utf_8')
    return

now = datetime.datetime.now()
now = now.strftime("%y%m%d")



# network
# audioSprite
# payload
# formdata
#data: {
# "brix_id":"CC0022_0003",
# "is_static_brix":"1",
# "format":"mp3",
# "duration_silent":15,
# "duration_distance":2,
# "000":"/html5v2/sound/correct.m4a.enc",
# "001":"/html5v2/sound/nocorrect.m4a.enc",
# "002":"v6/data/snd_m4a/word/ANF010/ANF010-competence.m4a.enc",
# "003":"v6/data/snd_m4a/word/ANF010/ANF010-concerned.m4a.enc",
# "004":"v6/data/snd_m4a/word/ANF010/ANF010-congress.m4a.enc",
# "005":"v6/data/snd_m4a/word/ANF010/ANF010-cure.m4a.enc",
# "006":"v6/data/snd_m4a/word/ANF010/ANF010-encounter.m4a.enc",
# "007":"v6/data/snd_m4a/word/ANF010/ANF010-grand.m4a.enc",
# "008":"v6/data/snd_m4a/word/ANF010/ANF010-intent.m4a.enc",
# "009":"v6/data/snd_m4a/word/ANF010/ANF010-profession.m4a.enc",
# "010":"v6/data/snd_m4a/word/ANF010/ANF010-runny_nose.m4a.enc",
# "011":"v6/data/snd_m4a/word/ANF010/ANF010-unlock.m4a.enc"
# }