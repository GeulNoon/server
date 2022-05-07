import email
from http.client import HTTPResponse
from importlib.resources import contents
from pickle import FALSE
from urllib import response
from django.shortcuts import render
from rest_framework import generics
from django.http import JsonResponse, HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
import bcrypt
import jwt 
import torch
from transformers.models.bart import BartForConditionalGeneration
from transformers import PreTrainedTokenizerFast
from .key import SECRET_KEY, ALGORITHM
from random import randint
import random
import json
from collections import OrderedDict
from django.utils import timezone
import requests
from bs4 import BeautifulSoup
import urllib3
from .models import User, ArticleQuiz, Study
from .serializers import UserSerializer, ArticleQuizSerializer, StudySerializer
from .article_comprehension import compute
from .get_keywords import getKeywords#4.30추가
from .keyword_score import computeKeywordScore#4.30추가
from django.db.models import Avg,Count#5.01추가
from django.db.models.functions import TruncMonth, TruncWeek, TruncDay#5.01추가
from datetime import datetime
from .exam_word import wordList
from .Word import test01, test02, test03


class ListPost(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class DetailPost(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

model = BartForConditionalGeneration.from_pretrained('./kobart_summary')
model3 = BartForConditionalGeneration.from_pretrained('./kobart_summary3')#5.01추가
tokenizer = PreTrainedTokenizerFast.from_pretrained('gogamza/kobart-base-v1')

# quiz content fake data
data1 = {
    'employees' : [
        {
            'name' : 'John Doe',
            'department' : 'Marketing',
            'place' : 'Remote'
        }
    ]
}

def models(article, keywordlist) : #4.30추가 summary json파일에 keyword 리스트도 저장
    
    text = article
    
    #지문(text)를 요약하는 과정(요약결과:output)
    text = text.replace('\n', '')
    input_ids = tokenizer.encode(text)
    input_ids = torch.tensor(input_ids)
    input_ids = input_ids.unsqueeze(0)
    output = model.generate(input_ids, eos_token_id=1, max_length=512, num_beams=5)
    output = tokenizer.decode(output[0], skip_special_tokens=True)

    #5.01추가
    input_ids_3 = tokenizer.encode(text)
    input_ids_3 = torch.tensor(input_ids_3)
    input_ids_3 = input_ids_3.unsqueeze(0)
    output_3 = model3.generate(input_ids_3, eos_token_id=1, max_length=512, num_beams=5)
    output_3 = tokenizer.decode(output_3[0], skip_special_tokens=True)
    
    #요약결과(output)를 토대로 문제 생성    
    content = output.split(' ')
    answerlist = []
    for i in range(len(content) - 1):
        if i % 2 == 0:
            answerlist.append(content[i]+" "+content[i+1])
    if len(content) % 2 != 0:
        answerlist.append(content[len(content)-1])
    text= text.replace('.', ' ')
    randoms = text.split(' ')
    randomlist = []
    for i in range(len(randoms) - 1):
        if i % 2 == 0:
            randomlist.append(randoms[i]+" "+randoms[i+1])
    randomlist = random.sample(randomlist,len(answerlist))
    answerlist += randomlist
    random.shuffle(answerlist)

    s1 = []
    s2 = []
    s3 = []

    for k in [x for x in keywordlist if len(x) > 1]: 
        if k in output_3.split('. ')[0]:
            s1.append(k)
        if k in output_3.split('. ')[1]:
            s2.append(k)
        if k in output_3.split('. ')[2]:
            s3.append(k)
    
    file_data = OrderedDict()
    #content: 블록배열을 위한 단어배열(본문 속 무작위 단어 + 요약문 단어)
    file_data["content"] = answerlist
    #answer: 요약문 정답
    file_data["answer"] = output
    file_data["answer_3"] = output_3 #5.01추가
    file_data["keyword"] = keywordlist #4.30추가 summary json파일에 keyword 리스트도 저장
    file_data["s1"] = s1
    file_data["s2"] = s2
    file_data["s3"] = s3
    
    #json파일(DB에 저장할 json파일 생성)
    jsonfile = json.dumps(file_data, ensure_ascii=False)
    
    #DB에 저장하는 과정 필요
    
    return jsonfile

id_now = [] # 현재 학습하는 지문 id (임시)
s_id_now = [] # 현재 학습하는 학습 id (임시)

# jWT 현재 사용 X
"""def get_user_email(request):
    token = request.headers.get('Authorization')
    if token is None:
        return None
    payload = jwt.decode(token, SECRET_KEY, ALGORITHM)
    return payload['email']"""

# 회원 가입
@api_view(['POST','GET'])
def SignUp(request) :
    if request.method == 'POST':
        hased_pw = bcrypt.hashpw(request.data['password'].encode('utf-8'), bcrypt.gensalt())
        decoded_hashed_pw = hased_pw.decode('utf-8')
        User.objects.create(
            email = request.data['email'],
            nickname = request.data['nickname'],
            password = decoded_hashed_pw,
            birthyear= request.data['birthyear'],
        )
        return JsonResponse(request.data, safe=False)
    return JsonResponse(status=401, safe=False)

# 로그인
@api_view(['POST','GET'])
def LogIn(request) :
    if request.method == 'POST':
        if User.objects.filter(email = request.data['email']).exists():
            user = User.objects.get(email = request.data['email'])
            if bcrypt.checkpw(request.data['password'].encode('utf-8'), user.password.encode('utf-8')) :
                token = jwt.encode({'email' : request.data['email']}, SECRET_KEY, ALGORITHM)   
                return JsonResponse({"token" : token}, status=200)
            else:
                return HttpResponse(status=401, safe=False)
        else:
            return JsonResponse(status=401, safe=False)
    return HttpResponse(status=401, safe=False)

# 지문 입력
@api_view(['POST','GET'])
def EnterArticle(request) :
    id = 0
    s_id = 0
    if request.method == 'POST':
        id_is_unique = True
        s_id_is_unique = True
        while id_is_unique:
            id = randint(1, 2147483647) # 지문 아이디 생성
            id_is_unique = ArticleQuiz.objects.filter(article_id=id).exists()
        while s_id_is_unique:
            s_id = randint(1, 2147483647) # 학습 아이디 생성
            s_id_is_unique = Study.objects.filter(study_id=s_id).exists()

        keywordlist = getKeywords(request.data['content'])
        keywordQuiz = request.data['content']
        for i,word in enumerate(keywordlist):
            keywordQuiz = keywordQuiz.replace(word,'('+str(i+1)+')'+"_"*len(word))

        summary = models(request.data['content'], keywordlist) # 지문 요약문 생성

        ArticleQuiz.objects.create(
            article_id = id,
            article_count = 1,
            article_content = request.data['content'],
            article_title = request.data['title'],
            article_summary = summary,
            article_keyword = keywordQuiz,  #4.30추가
            quiz1_content =  0,
            quiz2_content = 0,
            quiz3_content = 0,
            quiz4_content = 0,
            quiz1_answer = 0,
            quiz2_answer = 0,
            quiz3_answer = 0, 
            quiz4_answer = 0,
            email_id = request.data['email'],
        )

        # 학습 DB에 학습 id / 학습 시작 시간 / 사용자 email / 지문 id 삽입
        Study.objects.create(
            study_id = s_id,
            study_date = timezone.now(),
            study_type = 0,
            user_summary = '',
            choice = 0,
            quiz_count = 1,
            quiz1_user_answer = '',
            quiz2_user_answer = '',
            quiz3_user_answer = '',
            quiz4_user_answer = '',
            quiz1_user_answer_correct = 0,
            quiz2_user_answer_correct = 0,
            quiz3_user_answer_correct = 0,
            quiz4_user_answer_correct = 0,
            article_comprehension = 0,
            quiz_score = 0,
            keyword_user_answer = 0,  #4.30추가
            keyword_score = 0,  #4.30추가
            issubmitted = False,
            email = request.data['email'],
            article_id = id,
        )
        data = {
            's_id': s_id,
            'a_id': id,
        }
        return JsonResponse(data, safe=False)
    return JsonResponse(status=401, safe=False)

@api_view(['POST', 'GET'])
def title(request):
    title = ''
    if request.method == 'GET':
        if ArticleQuiz.objects.filter(article_id=request.query_params['a_id']).exists():
            article = ArticleQuiz.objects.get(article_id=request.query_params['a_id'])
            title = article.article_title
        data ={
            'title': title
        }
        return JsonResponse(data)
    else :
            return JsonResponse(status=401, safe=False)

# 학습하기 1단계 (학습하는 지문의 제목과 원문을 보냄)
@api_view(['PUT', 'GET'])
def step1(request):
    content = ''
    if request.method == 'GET':
        if ArticleQuiz.objects.filter(article_id=request.query_params['a_id']).exists():
            if Study.objects.filter(study_id = request.query_params['s_id']).exists():
                article = ArticleQuiz.objects.get(article_id=request.query_params['a_id'])
                study = Study.objects.get(study_id = request.query_params['s_id'])
                content  = article.article_content
                issubmitted = study.issubmitted#5.01추가(문제 확인 용)
        data ={
            'content': content,
            'issubmitted' : issubmitted
        }
        return JsonResponse(data)
        
    if request.method == 'PUT':
        if ArticleQuiz.objects.filter(article_id=request.data['a_id']).exists():
            if Study.objects.filter(study_id = request.data['s_id']).exists():
                article = ArticleQuiz.objects.get(article_id=request.data['a_id']) 
                study = Study.objects.get(study_id = request.data['s_id'])
                text = article.article_content
                temp = text.split(". ")
                wordlist = wordList(temp)
                q1= json.loads(test01.t01(wordlist[0]))
                q2 = json.loads(test02.t02(wordlist[1], temp))
                q3 = json.loads(test02.t02(wordlist[2], temp))
                q4 = json.loads(test03.t03(wordlist[3]))
                article.quiz1_content = q1
                article.quiz2_content = q2
                article.quiz3_content = q3
                article.quiz4_content = q4
                article.quiz1_answer = wordlist[0]
                article.quiz4_answer = wordlist[3]
                a = list(q1["CHOICE"].keys())
                b = list(q2["CHOICE"].values())
                c = list(q3["CHOICE"].values())
                d = list(q4["CHOICE"].keys())
                random.shuffle(a)
                random.shuffle(b)
                random.shuffle(c)
                random.shuffle(d)
                choice = OrderedDict()
                choice["1"] = a
                choice["2"] = b
                choice["3"] = c
                choice["4"] = d
                answer2 = []
                answer3 = []

                for i in b:
                    for k, v in q2["CHOICE"].items():
                        if v == i: 
                            answer2.append(k)
                for j in c:
                    for k, v in q3["CHOICE"].items():
                        if v == j: 
                            answer3.append(k)

                article.quiz2_answer = answer2
                article.quiz3_answer = answer3
                study.choice = choice
                article.save()
                study.save()
                data ={
                    's2': "ok",
                }
                return JsonResponse(data)
    else :
            return JsonResponse(status=401, safe=False)

# 학습하기 2단계 (학습하는 지문의 제목과 요약문(json 형태)을 보냄)
@api_view(['PUT','GET'])
def step2(request):
    if request.method == 'GET':
        if ArticleQuiz.objects.filter(article_id=request.query_params['a_id']).exists():
            if Study.objects.filter(study_id = request.query_params['s_id']).exists():
                article = ArticleQuiz.objects.get(article_id=request.query_params['a_id'])
                study = Study.objects.get(study_id = request.query_params['s_id'])
                summary = article.article_summary
                issubmitted = study.issubmitted
                jsonObject = json.loads(summary)
        data ={
            'summary': jsonObject['content'],
            's1': jsonObject['s1'],
            's2': jsonObject['s2'],
            's3': jsonObject['s3'],
            'issubmitted' : issubmitted
        }
        return JsonResponse(data)

    if request.method == 'PUT':
        if isinstance(request.data['user_summary'], list) :
            summary = " ".join(request.data['user_summary'])
        else:
            summary = request.data['user_summary']
        if Study.objects.filter(study_id = request.query_params['s_id']).exists():
            study = Study.objects.get(study_id = request.query_params['s_id'])
            study.user_summary = summary
            study.save()
            return JsonResponse(request.data, safe=False)
    else :
        return JsonResponse(status=401, safe=False)

@api_view(['GET'])
def step4(request):
    if request.method == 'GET':
        if Study.objects.filter(study_id = request.query_params['s_id']).exists():
            study = Study.objects.get(study_id = request.query_params['s_id'])
            article = ArticleQuiz.objects.get(article_id=request.query_params['a_id'])
            if User.objects.filter(email = study.email).exists():
                user = User.objects.get(email = study.email)
                name = user.nickname
            answer = article.article_summary
            summary = json.loads(article.article_summary)
            user_summary = study.user_summary#5.01추가
            if(user_summary.count('.')<=1): #5.01추가 2문장이상일 경우 자동으로 3문장 답안으로 채점
                answer = summary['answer'] #5.01추가
            else:#5.01추가
                answer = summary['answer_3']#5.01추가
            keywordlist = summary['keyword'] #4.30추가
            
            quiz_score = 0
            q2_c = []
            q3_c = []
            q2 = study.quiz2_user_answer[1:-1].split(', ')
            a2 = article.quiz2_answer[1:-1].split(', ')
            q3 = study.quiz3_user_answer[1:-1].split(', ')
            a3 = article.quiz3_answer[1:-1].split(', ')

            if(article.quiz1_answer == study.quiz1_user_answer):
                study.quiz1_user_answer_correct = 1
                quiz_score += 25
            else : 
                study.quiz1_user_answer_correct = 0

            for i in range(len(q2)):
                if(a2[i] == q2[i]):
                    q2_c.append(1)
                else: 
                    q2_c.append(0)    
            study.quiz2_user_answer_correct = q2_c

            for i in range(len(q3)):
                if(a3[i] == q3[i]):
                    q3_c.append(1)
                else: 
                    q3_c.append(0)
            study.quiz3_user_answer_correct = q3_c 

            if(0 not in q2_c):
                    quiz_score += 25
            if(0 not in q3_c):
                    quiz_score += 25

            if(article.quiz4_answer == study.quiz4_user_answer):
                study.quiz4_user_answer_correct = 1
                quiz_score += 25
            else:
                study.quiz4_user_answer_correct = 0 
            
            study.quiz_score = quiz_score
            article_comprehension = compute(user_summary, answer, keywordlist)
            study.article_comprehension = article_comprehension
            keyword_user_answer = json.loads(study.keyword_user_answer)#4.30추가
            keyword_score = computeKeywordScore(keyword_user_answer, keywordlist)#4.30추가
            study.keyword_score = keyword_score#4.30추가
            study.issubmitted = True
            study.save()
        data ={
            'name' : name,
            'article_comprehension' : article_comprehension,
            'summary': answer,
            'keyword_score': keyword_score,#4.30추가
            'keyword_answer': keywordlist,#4.30추가
            'keyword_user_answer': keyword_user_answer,#4.30추가
        }
        return JsonResponse(data)

    else :
        return JsonResponse(status=401, safe=False)

@api_view(['PUT','GET'])
def step3(request):# 어휘 문제와 관련된 DB와의 작업이 여기에 들어갈 것 같아요
    if request.method == 'GET':
        if ArticleQuiz.objects.filter(article_id=request.query_params['a_id']).exists():
            if Study.objects.filter(study_id = request.query_params['s_id']).exists():
                article = ArticleQuiz.objects.get(article_id=request.query_params['a_id'])
                study = Study.objects.get(study_id = request.query_params['s_id'])
                quiz1 = dict()
                quiz2 = dict()
                quiz3 = dict()
                quiz4 = dict()
                quiz1["Test"] = article.quiz1_content["TEST1"]
                quiz1["Choice"] = study.choice["1"]
                quiz2["Test"] = article.quiz2_content["TYPE2"]
                quiz2["Word"] = article.quiz2_content["WORD"]
                quiz2["Sentence"] = ''.join(article.quiz2_content["SENTENCE"])
                quiz2["MEAN"] = list(article.quiz2_content["CHOICE"].keys())
                quiz2["Choice"] = study.choice["2"]
                quiz2_user_answer = []#5.04추가 사용자 답안 받아올 배열 미리 생성
                for i in range(len(quiz2["Choice"])):
                    quiz2_user_answer.append({'id': i, 'value': ''})
                quiz2["User_answer"] = quiz2_user_answer
                quiz3["Test"] = article.quiz3_content["TYPE2"]
                quiz3["Word"] = article.quiz3_content["WORD"]
                quiz3["Sentence"] = ''.join(article.quiz3_content["SENTENCE"])
                quiz3["MEAN"] = list(article.quiz3_content["CHOICE"].keys())
                quiz3["Choice"] = study.choice["3"]
                quiz3_user_answer = []#5.04 추가 사용자 답안 받아올 배열 미리 생성
                for i in range(len(quiz3["Choice"])):
                    quiz3_user_answer.append({'id': i, 'value': ''})
                quiz3["User_answer"] = quiz3_user_answer
                quiz4["Test"] = article.quiz4_content["MEAN"]
                quiz4["Choice"] = study.choice["4"]
                issubmitted = study.issubmitted

                data ={
                'quiz1' : quiz1,
                'quiz2' : quiz2,
                'quiz3' : quiz3,
                'quiz4' : quiz4,
                'issubmitted' : issubmitted
        }
        return JsonResponse(data)

    if request.method == 'PUT':
        if Study.objects.filter(study_id = request.query_params['s_id']).exists():
            q1 = request.data['answer'][0]
            q2 = request.data['answer'][1]
            q3 = request.data['answer'][2]
            q4 = request.data['answer'][3]
            study = Study.objects.get(study_id = request.query_params['s_id'])
            study.quiz1_user_answer = q1['value']
            study.quiz2_user_answer = q2['value']
            study.quiz3_user_answer = q3['value']
            study.quiz4_user_answer = q4['value']
            study.save()
            return JsonResponse(request.data, safe=False)
    else :
        return JsonResponse(status=401, safe=False)

@api_view(['PUT','GET']) #4.30추가
def step5(request):
    if request.method == 'GET':
        if ArticleQuiz.objects.filter(article_id=request.query_params['a_id']).exists():
            if Study.objects.filter(study_id = request.query_params['s_id']).exists():
                article = ArticleQuiz.objects.get(article_id=request.query_params['a_id'])
                study = Study.objects.get(study_id = request.query_params['s_id'])
                keyword = article.article_keyword
                issubmitted = study.issubmitted
                summary = json.loads(article.article_summary)
                keywordlist = summary['keyword']
                answerlist = []
                for i,j in enumerate(keywordlist):
                    answerlist.append({'id': i, 'value': '0'})
                a = json.dumps(answerlist)
                answerjson = json.loads(a)
        data ={
            'keyword': keyword,
            'issubmitted' : issubmitted,
            'answerlist' : answerjson
        }
        return JsonResponse(data)
    
    if request.method == 'PUT':
        print(request.data['answer'])
        if Study.objects.filter(study_id = request.query_params['s_id']).exists():
            study = Study.objects.get(study_id = request.query_params['s_id'])
            keyword_dict = OrderedDict()
            keyword_dict["answer"] = request.data['answer']
            #json파일(DB에 저장할 json파일 생성)
            keyword_json = json.dumps(keyword_dict, ensure_ascii=False)
            study.keyword_user_answer = keyword_json
            study.save()
            return JsonResponse(request.data, safe=False)
        return JsonResponse(request.data, safe=False)
        
    else :
        return JsonResponse(status=401, safe=False)
    

# 마이페이지 
@api_view(['DELETE', 'GET', 'PUT'])
def Mypage(request):
    if request.method == 'GET':
        if User.objects.filter(email = request.query_params['email']).exists():
            user = User.objects.get(email = request.query_params['email'])
            nickname = user.nickname
            birthyear = user.birthyear
        data ={
            'nickname': nickname,
            'birthyear': birthyear
        }
        return JsonResponse(data)

    if request.method == 'DELETE':
        if User.objects.filter(email = request.data['email']).exists():
            user = User.objects.get(email = request.data['email'])
            user.delete()
            
        data = {
                'delete': 'ok'
        }
        return JsonResponse(data)
    if request.method == 'PUT':
        if User.objects.filter(email = request.data['email']).exists():
            user = User.objects.get(email = request.data['email'])
            if(request.data['password']):
                hased_pw = bcrypt.hashpw(request.data['password'].encode('utf-8'), bcrypt.gensalt())
                decoded_hashed_pw = hased_pw.decode('utf-8')
                user.password = decoded_hashed_pw
            if('nickname' in request.data):   
                if(request.data['nickname']):
                    user.nickname = request.data['nickname']
            if('birthyear' in request.data):    
                user.birthyear= request.data['birthyear']
            user.save()
        data = {
                'edit': 'ok'
        }
        return JsonResponse(data)
    else :
            return JsonResponse(status=401, safe=False)

# 단어 검색
@api_view(['POST','GET'])
def searchWord(request):
    if request.method == 'POST':
        url = "https://krdict.korean.go.kr/api/search?"
        serviceKey = "certkey_no=3341&key=A715599AC7951FC091E0810CAA1EC810"
        typeOfSearch="&type_search=search"
        part = "&part=word"
        word = request.data["word"]
        sort = "&sort=popular"

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
        #parsing 하기
        result = requests.get(url+serviceKey+typeOfSearch+part+"&q="+word+sort, verify=False)
        soup = BeautifulSoup(result.text,'lxml-xml')
        items = soup.find_all("item")
        row = []
        for item in items:
            WORD = item.find("word").get_text()
            if WORD == word:
                definition = parse()
                row.append(definition['뜻'])
        data ={
            'definition': row,
        }
        return JsonResponse(data)
    else :
            return JsonResponse(status=401, safe=False)
        
#질의응답
@api_view(['POST','GET'])
def getAnswer(request):
    if request.method == 'POST':
        content=''
        if ArticleQuiz.objects.filter(article_id=request.query_params['a_id']).exists():
            article = ArticleQuiz.objects.get(article_id=request.query_params['a_id'])
            content  = article.article_content
        openApiURL = "http://aiopen.etri.re.kr:8000/MRCServlet"
        accessKey = "ed2296ff-a698-42e2-b72a-49fca2265500"
        question = request.data["question"]
        passage = content
        
        requestJson = {
        "access_key": accessKey,
            "argument": {
                "question": question,
                "passage": passage
            }
        }
        
        http = urllib3.PoolManager()
        response = http.request(
            "POST",
            openApiURL,
            headers={"Content-Type": "application/json; charset=UTF-8"},
            body=json.dumps(requestJson)
        )
        datas = json.loads(response.data)
        data ={
            'answer': datas['return_object']['MRCInfo']['answer'],
        }
        return JsonResponse(data)
    else :
            return JsonResponse(status=401, safe=False)

# 학습기록 요약버전
@api_view(['GET'])
def GetHistory(request):
    if request.method == 'GET':
        titlelist = []
        total_study = 0 #매칭되는 id 없을 시 local variable '...' referenced before assignment error 처리용
        avg_article_comprehension = 0 #5.03 추가
        avg_word_score = 0 #5.03 추가
        if User.objects.filter(email = request.query_params['email']).exists():
            user = User.objects.get(email = request.query_params['email'])
            if Study.objects.filter(email = user.email).exists():
                study = Study.objects.filter(email = user.email)
                total_study = len(study)
                avg_article_comprehension =  study.aggregate(Avg('article_comprehension'))['article_comprehension__avg']
                avg_keyword_score = study.aggregate(Avg('keyword_score'))['keyword_score__avg']#4.30추가
                avg_article_comprehension = (avg_article_comprehension+avg_keyword_score)/2#5.03추가
                avg_word_score = study.aggregate(Avg('quiz_score'))['quiz_score__avg']#5.03추가
                for i,s in enumerate(study.order_by('-study_date')): # 최근 학습 시간이 상단으로
                    date = s.study_date.strftime("%Y-%m-%d %H:%M:%S") 
                    id = s.article_id
                    if ArticleQuiz.objects.filter(article_id = id).exists():
                        article = ArticleQuiz.objects.get(article_id = id)
                        title = article.article_title
                    titlelist.append([title,date])
                    if i == 4: break
            
        data ={
            'title': titlelist,
            'total_study': total_study,
            'avg_article_comprehension': round(avg_article_comprehension, 1),
            'avg_word_score' : round(avg_word_score, 1)#5.03추가
        }
        return JsonResponse(data)
    else :
            return JsonResponse(status=401, safe=False)
        
#5.01추가
@api_view(['GET'])
def GetStatistics(request):
    if request.method == 'GET':
        study_count = []#5.03 추가
        study_avg = []#5.03 추가
        if User.objects.filter(email = request.query_params['email']).exists():
            user = User.objects.get(email = request.query_params['email'])
            if Study.objects.filter(email = user.email).exists():
                study = Study.objects.filter(email = user.email)
                if request.query_params['option'] == '0':
                    study_count = study.annotate(day=TruncDay('study_date')).values('day').annotate(cnt=Count('study_id')).values('day', 'cnt').order_by('-day')[:5]
                    study_avg = study.annotate(day=TruncDay('study_date')).values('day').annotate(avg1=Avg('article_comprehension'), avg2=Avg('quiz_score'), avg3=Avg('keyword_score')).values('day', 'avg1','avg2','avg3').order_by('-day')[:5]
                elif  request.query_params['option'] == '1':
                    study_count = study.annotate(day=TruncWeek('study_date')).values('day').annotate(cnt=Count('study_id')).values('day', 'cnt').order_by('-day')[:5]
                    study_avg = study.annotate(day=TruncWeek('study_date')).values('day').annotate(avg1=Avg('article_comprehension'), avg2=Avg('quiz_score'), avg3=Avg('keyword_score')).values('day', 'avg1','avg2','avg3').order_by('-day')[:5]
                elif  request.query_params['option'] == '2':
                    study_count = study.annotate(day=TruncMonth('study_date')).values('day').annotate(cnt=Count('study_id')).values('day', 'cnt').order_by('-day')[:5]
                    study_avg = study.annotate(day=TruncMonth('study_date')).values('day').annotate(avg1=Avg('article_comprehension'), avg2=Avg('quiz_score'), avg3=Avg('keyword_score')).values('day', 'avg1','avg2','avg3').order_by('-day')[:5]
        
        for x, y in zip(study_count, study_avg):
            x['day'] = x['day'].strftime("%Y-%m-%d %H:%M:%S")
            y['day'] = y['day'].strftime("%Y-%m-%d %H:%M:%S")
            
        '''for x in study_count:
            x['day'] = x['day'].strftime("%Y-%m-%d %H:%M:%S") '''

        data ={
            'study_count':list(study_count),
            'study_avg':list(study_avg)
        }
        return JsonResponse(data)
    else :
            return JsonResponse(status=401, safe=False)
        
# 학습기록 더보기
@api_view(['POST','GET'])
def GetMoreHistory(request):
    if request.method == 'GET':
        titlelist = []
        if User.objects.filter(email = request.query_params['email']).exists():
            user = User.objects.get(email = request.query_params['email'])
            if Study.objects.filter(email = user.email).exists():
                study = Study.objects.filter(email = user.email)
                for s in study.order_by('-study_date'):
                    date = s.study_date.strftime("%Y-%m-%d %H:%M:%S")
                    step2_score = s.article_comprehension
                    step3_score = s.quiz_score
                    step4_score = s.keyword_score#4.30추가
                    s_id = s.study_id
                    id = s.article_id
                    if ArticleQuiz.objects.filter(article_id = id).exists():
                        article = ArticleQuiz.objects.get(article_id = id)
                        title = article.article_title
                        a_id = article.article_id
                    titlelist.append([title,date,step2_score,step3_score,step4_score,a_id,s_id])#4.30추가
            
        data ={
            'title': titlelist,
        }
        return JsonResponse(data)
    else :
            return JsonResponse(status=401, safe=False)

# 오답노트 기능 5.03 추가
@api_view(['PUT','GET'])
def ReviewStudy(request):
    s_id = 0
    if request.method == 'PUT':
        if ArticleQuiz.objects.filter(article_id=request.data['a_id']).exists():
            s_id_is_unique = True
            while s_id_is_unique:
                s_id = randint(1, 2147483647) # 학습 아이디 생성
                s_id_is_unique = Study.objects.filter(study_id=s_id).exists()
            Study.objects.create(
            study_id = s_id,
            study_date = timezone.now(),
            study_type = 1, # 재학습
            user_summary = '',
            quiz_count = 1,
            quiz1_user_answer = '',
            quiz2_user_answer = '',
            quiz3_user_answer = '',
            quiz4_user_answer = '',
            quiz1_user_answer_correct = 0,
            quiz2_user_answer_correct = 0,
            quiz3_user_answer_correct = 0,
            quiz4_user_answer_correct = 0,
            article_comprehension = 0,
            quiz_score = 0,
            keyword_user_answer = data1,  #4.30추가
            keyword_score = 0,  #4.30추가
            issubmitted = False,
            email = request.data['email'],
            article_id = request.data['a_id'],
        )
        data ={
            's_id': s_id
        }
        return JsonResponse(data)
    else :
            return JsonResponse(status=401, safe=False)

