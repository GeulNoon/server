# -*- coding: utf-8 -*-
from konlpy.tag import Kkma
import itertools
import json
from collections import OrderedDict
import requests
from bs4 import BeautifulSoup
import os
import random
from .Word.exam_func import TEST, EXAMPLE
from gensim.models import Word2Vec

def wordList(temp):
    #불용어제거 리스트
    ko_model = Word2Vec.load('./ko/ko_new.bin')
    module_dir = os.path.dirname(__file__) 

    with open(os.path.join(module_dir, 'stop_word.txt'), encoding = 'cp949') as f:
        stop_word = f.readlines()
        f.close()

    # 출제기준1 (A,B,C)
    with open(os.path.join(module_dir, 'WORD_A_01.txt'),encoding = 'cp949') as f:
        WORD_A_01 = f.readlines()
        f.close()
        
    # 불용어 제거_리스트파일로 바꾸기
    stopwords = list(itertools.chain(*stop_word))
    no_contain = [',']

    stopword = [i for i in stopwords if i not in no_contain]

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

    WORD = TEXT_WORD(temp,stopword)

    # 출제기준 어휘 데이터 처리
    # (리스트 안에 한개의 문자열로 되어 있어 분리하는 작업)
    def TOList_A1(WORD_A_01):
    # 문자열 한개 -> 여러개로 쪼개기
        stringA1 = ''.join(WORD_A_01)
    # ,를 기준으로 분리
        A01 = stringA1.split(',')
    
        return A01

    # 출제기준1&2 - 상(A) 리스트
    def EXAM_A1(A01):
        exam_A_01 = []
        for i in WORD:
            if i in A01:
                if i not in exam_A_01:
                    exam_A_01.append(i)
        return exam_A_01

    
    word_A_01 = EXAM_A1(TOList_A1(WORD_A_01))

    def SAMEWORD(word_A_01):        
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
                if len(i) > 1:
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

    #출제 어휘 선정
    word02 = []
    similar_list = []
    for i in test_sameword:
        t = TEST(i)
        result_example = t[1]
        ex_example = EXAMPLE(result_example)
        if ex_example:
            word02.append(i)
        similar = t[2]
        if similar:
            similar_list.append(i)
    print(word02)
    print(similar_list)
    if not word02:
        word.append("전면")
    else:
        word = random.sample(word02,1)
    
    if not similar_list:
        word.append("반박")
    else:
        word.append(random.choice(similar_list))

    word0103 = []

    for i in test_word:
        w = ko_model.wv.most_similar(i)
        if w :
            word0103.append(i)
    if len(word0103) == 0:
        word0103.append("신규")
        word0103.append("유입")
    elif len(word0103) == 1:
        word0103.append("신규")
    
    word_0103 = random.sample(word0103, 2)

    word.insert(0,word_0103[0])
    word.append(word_0103[1])
    
    return word