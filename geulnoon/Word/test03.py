from .exam_func import TEST, MEAN,EXAMPLE, EXAMPLE_test
import json
from collections import OrderedDict
from .W2V_word import W2V

# 콤마, 괄호 삭제
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

#W2V 어휘들 뜻
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

#exam_word에서 뽑아온 3번문제 어휘
def t03(word):

    #W2V_word에서 뽑아온 보기 어휘
    w2v_word = W2V(word)

    #parsing에서 코드 추출
    t = TEST(word)
    result_parse = t[0]
    result_example = t[1]

    # 뜻 추출
    ex_mean = MEAN(result_parse)

    mean = REMOVE(ex_mean)

    w2v_mean = W2V_MEAN(w2v_word)

    w2v_mean = W2V_MEAN(w2v_word)

    choice = { name:value for name, value in zip(w2v_word, w2v_mean) }
    choice[word] = mean

    #json파일
    #문제 3번은 MEAN 문제, WORD 정답
    file_exam3 = OrderedDict()
    file_exam3["TYPE3"] = "다음 단어들 중 주어진 사전적 의미에 부합하는 가장 적절한 단어를 고르시오."
    file_exam3["ANSWER"] = word    #단어
    file_exam3["MEAN"] = mean    #뜻
    #file_exam3["W2VWORD"] = w2v_word    #보기 단어
    #file_exam3["W2VMEAN"] = w2v_mean    #보기 단어 뜻
    file_exam3["CHOICE"] = choice

    #json파일
    EXAM3 = json.dumps(file_exam3, ensure_ascii=False, indent="\t")
    return EXAM3
