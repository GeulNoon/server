# -*- coding: utf-8 -*-
from sentence_transformers import SentenceTransformer, util
import networkx
import re
import os 

model = SentenceTransformer("./sentence-transformers")
    
# 대부분 이부분 아래부터 수정하였습니다.

def compute (sentence_length, user_summary, answer, keywordlist): #4.30수정 text 대신 keywordlist 바로 받아오는 것으로 변경
    if(sentence_length == 1):
        embeddings_user = model.encode(user_summary, convert_to_tensor=True)
        embeddings_answer = model.encode(answer, convert_to_tensor=True)

        cosine_score = util.pytorch_cos_sim(embeddings_user, embeddings_answer)[0]

        sim = float(cosine_score[0])
        if(sim < 0):
            sim = 0

        words = []
        
        for k in keywordlist:  #4.30수정
            if (len(k)>1) :
                if k in answer:
                    words.append(k)
        keyword = 0

        for word in words:
            inc = word in user_summary 
            if (inc  == True):
                keyword += 1

        try:
            kw_in_sentence = keyword/len(words)
            summary_score = sim * (0.6) + kw_in_sentence * (0.4)
        except:
            summary_score = sim
            
        print(summary_score)
        return round(summary_score * 100)
    else:
        a = answer.split(". ")
        summary_score = [0, 0, 0]
        for i in range(3):
            if (user_summary[i]):
                embeddings_user = model.encode(user_summary[i], convert_to_tensor=True)
                embeddings_answer = model.encode(a[i] + ('.'), convert_to_tensor=True)

                cosine_score = util.pytorch_cos_sim(embeddings_user, embeddings_answer)[0]

                sim = float(cosine_score[0])
                if(sim < 0):
                    sim = 0

                key = "s" + str(i+1)
                keyword = 0
                for word in keywordlist[key]:
                    inc = word in user_summary[i]
                    if (inc  == True):
                        keyword += 1

                kw_in_sentence = keyword/len(keywordlist[key])
                summary_score[i] = sim * (0.9) + kw_in_sentence * (0.1)  * 100
            else:
                summary_score[i] = 0
        return round(sum(summary_score) / 3)
