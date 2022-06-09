#from exam_word import word_04
from .exam_func import TEST, MEAN,EXAMPLE, EXAMPLE_test, SIMILAR
import json
from collections import OrderedDict
from .W2V_word import W2V
import random

# word = word_04

def REMOVE(st):
    row = ' '.join(s for s in st)
    remove = "}"
    for x in range(len(remove)):
      row1 = row.replace(remove[x],"")
    row2 = row1.replace("'","")
    row3 = row2.split('.')
    strip_li = []
    for i in row3:
        i = i.strip()
        if i:
          strip_li.append(i)
        
    return strip_li

def W2V_MEAN(w2v_word):
    n = len(w2v_word)
    w2v_mean = []
    for i in range(0,n):
        t = TEST(w2v_word[i])
        result_parse = t[0]
        row1 = MEAN(result_parse)
        row2 = REMOVE(row1)
        w2v_mean.append(row2)
    
    return w2v_mean

def t04(word):
    
    w2v_word = W2V(word)

    t = TEST(word)
    result_parse = t[0]
    result_similar = t[2]
    result_similar = random.choice(result_similar)
    
    mean = result_similar['예시']
    similar = result_similar['유의어']
    similar_list = []
    similar_list.append(similar)
    
    w2v_mean = W2V_MEAN(w2v_word) + W2V_MEAN(similar_list)
    w2v_word = w2v_word + similar_list
    
    choice = { name:value for name, value in zip(w2v_word, w2v_mean) }
    
    file_exam4 = OrderedDict()
    file_exam4["TYPE4"] = "다음 문장 속 "+word+"의 의미와 가장 관련이 깊은 단어를 고르시오."
    #file_exam4["WORD"] = word    #단어
    file_exam4["ANSWER"] = similar    #유의어
    file_exam4["MEAN"] = mean    #뜻
    file_exam4["CHOICE"] = choice

    EXAM4 = json.dumps(file_exam4, ensure_ascii=False, indent="\t")
    print(EXAM4)
    return EXAM4
