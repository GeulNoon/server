from konlpy.tag import Kkma
import matplotlib.pyplot as plt
from collections import Counter
from gensim.models import Word2Vec
import random

def W2V(word):

    ko_model = Word2Vec.load("././ko/ko_new.bin")#디렉토리 수정
    example = ko_model.wv.most_similar(word)
    print(example)
    
    word_list = []
    try:
        for i in range(3, len(example)):
            if len(example[i][0]) > 1 :
                word_list.append(example[i][0])
    except:
        word_list = example
    
    w2v_word = []
    w2v_word = random.sample(word_list,  4)

    return w2v_word