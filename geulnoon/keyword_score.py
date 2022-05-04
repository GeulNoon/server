#4.30 추가 빈칸문제 채점
from logging import exception
import gensim #pip install gensim==3.8.1

ko_model = gensim.models.Word2Vec.load('./ko/ko.bin') #ko.bin 모델 필요
def computeKeywordScore (user_answer, answer): 
    user_answer_list = user_answer['answer']
    score = 0
    for i in range(len(user_answer_list)):
        if user_answer_list[i]['value'] == answer[i]:
            score += 1
        else:
            try:
                similarity = ko_model.wv.similarity(user_answer_list[i]['value'],answer[i])
                if similarity >= 0.9:
                    score += 1
            except:
                print("단어가 없습니다!")
    return round(score/len(answer)*100,1)
