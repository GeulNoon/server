# -*- coding: utf-8 -*-
from konlpy.tag import Kkma
import itertools
import json
from collections import OrderedDict
import requests
from bs4 import BeautifulSoup
import os

def wordList(temp):
    #불용어제거 리스트
    module_dir = os.path.dirname(__file__) 

    with open(os.path.join(module_dir, 'stop_word.txt'), encoding = 'cp949') as f:
        stop_word = f.readlines()
        f.close()

    # 출제기준1 (A,B,C)
    with open(os.path.join(module_dir, 'WORD_A_01.txt'),encoding = 'cp949') as f:
        WORD_A_01 = f.readlines()
        f.close()

    with open(os.path.join(module_dir, 'WORD_B_01.txt'),encoding = 'cp949') as f:
        WORD_B_01 = f.readlines()
        f.close()

    with open(os.path.join(module_dir, 'WORD_C_01.txt'),encoding = 'cp949') as f:
        WORD_C_01 = f.readlines()
        f.close() 

    # 출제기준2(A,B,C)
    with open(os.path.join(module_dir, 'WORD_A_02.txt'),encoding = 'cp949') as f:
        WORD_A_02 = f.readlines()
        f.close()

    with open(os.path.join(module_dir, 'WORD_B_02.txt'),encoding = 'cp949') as f:
        WORD_B_02 = f.readlines()
        f.close()

    with open(os.path.join(module_dir, 'WORD_C_02.txt'),encoding = 'cp949') as f:
        WORD_C_02 = f.readlines()
        f.close()  
        
    # 불용어 제거_리스트파일로 바꾸기
    stopwords = list(itertools.chain(*stop_word))
    no_contain = [',']

    stopword = [i for i in stopwords if i not in no_contain]
    #print(stopword)

    # 지문에서 불용어 제거한 명사만 있는 리스트
    kkma = Kkma()
    text_word_list = []


    def TEXT_WORD(temp, stopword):
        for i in temp:
            nouns = kkma.nouns(i)
            for noun in nouns:
                if noun not in stopword:
                    text_word_list.append(noun)
                        
        return text_word_list

    # 출제기준 어휘 데이터 처리
    # (리스트 안에 한개의 문자열로 되어 있어 분리하는 작업)
    def TOList_A1(WORD_A_01):
        # 문자열 한개 -> 여러개로 쪼개기
        stringA1 = ''.join(WORD_A_01)
        # ,를 기준으로 분리
        A01 = stringA1.split(',')
        
        return A01

    def TOList_B1(WORD_B_01):
        stringB1 = ''.join(WORD_B_01)
        B01 = stringB1.split(',')
        
        return B01

    def TOList_C1(WORD_C_01):
        stringC1 = ''.join(WORD_C_01)
        C01 = stringC1.split(',')
        
        return C01

    def TOList_A2(WORD_A_02):
        stringA2 = ''.join(WORD_A_02)
        A02 = stringA2.split(',')
        
        return A02

    def TOList_B2(WORD_B_02):
        stringB2 = ''.join(WORD_B_02)
        B02 = stringB2.split(',')
        
        return B02

    def TOList_C2(WORD_C_02):
        stringC2 = ''.join(WORD_C_02)
        C02 = stringC2.split(',')
        
        return C02

    WORD = TEXT_WORD(temp,stopword)

    # 출제기준1&2 - 상(A) 리스트
    def EXAM_A1(A01):
        exam_A_01 = []
        for i in WORD:
            if i in A01:
                if i not in exam_A_01:
                    exam_A_01.append(i)
        return exam_A_01

    def EXAM_A2(A02):
        exam_A_02 = []
        for i in WORD:
            if i in A02:
                if i not in exam_A_02:
                    exam_A_02.append(i)
        return exam_A_02

    # 출제기준1&2 - 중(B) 리스트
    def EXAM_B1(B01):
        exam_B_01 = []
        for i in WORD:
            if i in B01:
                if i not in exam_B_01:
                    exam_B_01.append(i)
        return exam_B_01

    def EXAM_B2(B02):
        exam_B_02 = []
        for i in WORD:
            if i in B02 : 
                if i not in exam_B_02:
                    exam_B_02.append(i)
                    
        return exam_B_02

    # 출제기준1&2 - 하(C) 리스트
    def EXAM_C1(C01):
        exam_C_01 = []
        for i in WORD:
            if i in C01 : 
                if i not in exam_C_01:
                    exam_C_01.append(i)
                    
        return exam_C_01

    def EXAM_C2(C02):
        exam_C_02 = []
        for i in WORD:
            if i in C02 : 
                if i not in exam_C_02:
                    exam_C_02.append(i)
                    
        return exam_C_02

    word_All = EXAM_A1(TOList_A1(WORD_A_01))+EXAM_B1(TOList_B1(WORD_B_01))+EXAM_C1(TOList_C1(WORD_C_01))+EXAM_A2(TOList_A2(WORD_A_02))+EXAM_B2(TOList_B2(WORD_B_02))+EXAM_C2(TOList_C2(WORD_C_02))

    word_A_01 = EXAM_A1(TOList_A1(WORD_A_01))
    word_B_01 = EXAM_B1(TOList_B1(WORD_B_01))
    word_C_01 = EXAM_C1(TOList_C1(WORD_C_01))
    word_A_02 = EXAM_A2(TOList_A2(WORD_A_02))
    word_B_02 = EXAM_B2(TOList_B2(WORD_B_02))
    word_C_02 = EXAM_C2(TOList_C2(WORD_C_02))

    #동음이의어 리스트
    def SAMEWORD(word_A_01):        
        def parse():
            try:
                TGT = item.find("target_code").get_text()
                WORD = item.find("word").get_text()
                DEF = item.find("definition").get_text()
                return {
                    "코드":TGT,
                    "단어":WORD,
                    "뜻":DEF,
                    }

            except AttributeError as e:
                return {
                    "코드":None,
                    "단어":None,
                    "뜻":None,
                }
        def target_parse():
            try:
                TGT = item.find("target_code").get_text()
                return {
                    TGT,
                    }

            except AttributeError as e:
                return {
                    None,
                }

        url = "https://krdict.korean.go.kr/api/search?"
        serviceKey = "certkey_no=3349&key=EAE8B2C9214D808997D177C50333BBFA"
        typeOfSearch="&type_search=search"
        part = "&part=word"
        sort = "&sort=popular"

        ex_word = []

        for i in word_A_01:
            word = i
            requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)
            result = requests.get(url+serviceKey+typeOfSearch+part+"&q="+word+sort,verify=False)
            soup = BeautifulSoup(result.text,'lxml-xml')
            items = soup.find_all("item")

            target_row = []
            for item in items:
                WORD = item.find("word").get_text()
                if WORD == word:
                    target_row.append(str(target_parse())[2:7])

                    if len(target_row) > 1:
                        ex_word.append(word)
        
        sameword_list = []
        for i in ex_word:
            if i not in result:
                if len(i)>1:
                    sameword_list.append(i)   
            
        return sameword_list

    #동음이의어 제외한 어휘리스트        
    def WORD(word_A_01):
        sameword = SAMEWORD(word_A_01)
        word_list = []
        for word in word_A_01:
            if word not in sameword:
                if len(word)>1:
                    word_list.append(word)
                
        return word_list

    #리스트내에서 중복된 어휘 제거
    test_sameword = list(set(SAMEWORD(word_A_01)))
    test_word = list(set(WORD(word_A_01)))

    word_02 = test_sameword[:2]

    test_word.insert(1, word_02[0])
    test_word.insert(2, word_02[1])

    """#json파일로 변환 (다의어 목록, 다의어 제외 목록)
    file_word = OrderedDict()
    file_word["SAMEWORD"] = test_sameword
    file_word["WORD"] = test_word"""

    print(test_word)
    return test_word[:4]