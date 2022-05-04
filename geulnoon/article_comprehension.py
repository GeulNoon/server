# -*- coding: utf-8 -*-
from sentence_transformers import SentenceTransformer, util
import networkx
import re
import os 

model = SentenceTransformer("./sentence-transformers")
    
# 대부분 이부분 아래부터 수정하였습니다.

def compute (user_summary, answer, keywordlist): #4.30수정 text 대신 keywordlist 바로 받아오는 것으로 변경

    embeddings_user = model.encode(user_summary, convert_to_tensor=True)
    embeddings_answer = model.encode(answer, convert_to_tensor=True)

    cosine_score = util.pytorch_cos_sim(embeddings_user, embeddings_answer)[0]

    sim = float(cosine_score[0])
    if(sim < 0):
        sim = 0
    '''
    tr = TextRank(window=5, coef=1)
    stopword = set([('있', 'VV'), ('하', 'VV'), ('되', 'VV'), ('없', 'VV') ])
    tr.load(RawTaggerReader(text), lambda w: w not in stopword and (w[1] in ('NNG', 'NNP', 'VV', 'VA')))
    tr.build()
    kw = tr.extract(0.1)
    '''

    words = []
    
    for k in keywordlist:  #4.30수정
        if (len(k)>1) :
            if k in answer:
                words.append(k)
    '''           
    for k in kw.keys():
        for i in k:
            if (len(i[0]) > 1):
                if i[0] in answer:
                    words.append(i[0])
    ''' 
    keyword = 0

    for word in words:
        inc = word in user_summary 
        if (inc  == True):
            keyword += 1

    kw_in_sentence = keyword/len(words)
    summary_score = sim * (0.6) + kw_in_sentence * (0.4)
    return round(summary_score * 100)
