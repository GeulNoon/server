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
from django.db.models import Avg
from datetime import datetime


class ListPost(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = ArticleQuizSerializer

class DetailPost(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = ArticleQuizSerializer

model = BartForConditionalGeneration.from_pretrained('./kobart_summary')
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

def models(article) :
    
    text = article

    #지문(text)를 요약하는 과정(요약결과:output)
    text = text.replace('\n', '')
    input_ids = tokenizer.encode(text)
    input_ids = torch.tensor(input_ids)
    input_ids = input_ids.unsqueeze(0)
    output = model.generate(input_ids, eos_token_id=1, max_length=512, num_beams=5)
    output = tokenizer.decode(output[0], skip_special_tokens=True)

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

    file_data = OrderedDict()
    #content: 블록배열을 위한 단어배열(본문 속 무작위 단어 + 요약문 단어)
    file_data["content"] = answerlist
    #answer: 요약문 정답
    file_data["answer"] = output
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
    if request.method == 'POST':

        id_is_unique = True
        id = 0
        while id_is_unique:
            id = randint(1, 2147483647) # 지문 아이디 생성
            id_is_unique = ArticleQuiz.objects.filter(article_id=id).exists()
        id_now.append(id)

        s_id_is_unique = True
        s_id = 0
        while s_id_is_unique:
            s_id = randint(1, 2147483647) # 학습 아이디 생성
            s_id_is_unique = Study.objects.filter(study_id=s_id).exists()
        s_id_now.append(s_id)

        summary = models(request.data['content']) # 지문 요약문 생성

        # 어휘 문제 생성 함수는 여기에 들어 갈 것 같아요
        
        # 지문 DB에 사용자 지문 / 요약문 / 생성 문제 삽입
        ArticleQuiz.objects.create(
            article_id = id,
            article_count = 1,
            article_content = request.data['content'],
            article_title = request.data['title'],
            article_summary = summary,
            quiz1_content = data1,
            quiz2_content = data1,
            quiz3_content = data1,
            quiz4_content = data1,
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
            email = request.data['email'],
            article_id = id,
        )
        return JsonResponse(request.data, safe=False)
    return JsonResponse(status=401, safe=False)

# 학습하기 1단계 (학습하는 지문의 제목과 원문을 보냄)
@api_view(['GET'])
def step1(request):
    title = ''
    content = ''
    if request.method == 'GET':
        if ArticleQuiz.objects.filter(article_id=id_now[0]).exists():
            article = ArticleQuiz.objects.get(article_id=id_now[0])
            title = article.article_title
            content  = article.article_content
        data ={
            'title': title,
            'content': content
        }
        return JsonResponse(data)
    else :
            return JsonResponse(status=401, safe=False)

# 학습하기 2단계 (학습하는 지문의 제목과 요약문(json 형태)을 보냄)
@api_view(['PUT','GET'])
def step2(request):
    if request.method == 'GET':
        if ArticleQuiz.objects.filter(article_id=id_now[0]).exists():
            article = ArticleQuiz.objects.get(article_id=id_now[0])
            title = article.article_title
            summary = article.article_summary
            jsonObject = json.loads(summary)
        data ={
            'title' : title,
            'summary': jsonObject['content'],
        }
        return JsonResponse(data)

    if request.method == 'PUT':
        if isinstance(request.data['user_summary'], list) :
            summary = " ".join(request.data['user_summary'])
        else:
            summary = request.data['user_summary']
        if Study.objects.filter(study_id = s_id_now[0]).exists():
            study = Study.objects.get(study_id = s_id_now[0])
            study.user_summary = summary
            study.save()
            return JsonResponse(request.data, safe=False)
    else :
        return JsonResponse(status=401, safe=False)

@api_view(['GET'])
def step4(request):
    if request.method == 'GET':
        if Study.objects.filter(study_id = s_id_now[0]).exists():
            study = Study.objects.get(study_id = s_id_now[0])
            article = ArticleQuiz.objects.get(article_id=id_now[0])
            title = article.article_title
            text = article.article_content
            answer = article.article_summary
            summary = json.loads(article.article_summary)
            answer = summary['answer']
            user_summary = study.user_summary
            article_comprehension = compute(text, user_summary, answer)
            study.article_comprehension = article_comprehension
            study.save()
            data ={
            'title' : title,
            'article_comprehension' : article_comprehension,
            'summary': answer
        }
        return JsonResponse(data)

    else :
        return JsonResponse(status=401, safe=False)

    
    
        
"""@api_view(['POST','GET'])
def step3(request):""" # 어휘 문제와 관련된 DB와의 작업이 여기에 들어갈 것 같아요 

# 마이페이지 
@api_view(['POST','GET'])
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
        if ArticleQuiz.objects.filter(article_id=id_now[0]).exists():
            article = ArticleQuiz.objects.get(article_id=id_now[0])
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
@api_view(['POST','GET'])
def GetHistory(request):
    if request.method == 'GET':
        titlelist = []
        if User.objects.filter(email = request.query_params['email']).exists():
            user = User.objects.get(email = request.query_params['email'])
            if Study.objects.filter(email = user.email).exists():
                study = Study.objects.filter(email = user.email)
                total_study = len(study)
                avg_article_comprehension =  study.aggregate(Avg('article_comprehension'))['article_comprehension__avg']
                print(avg_article_comprehension)

                for i,s in reversed(list(enumerate(study))):
                    date = s.study_date.strftime("%Y-%m-%d %H:%M:%S")
                    id = s.article_id
                    if ArticleQuiz.objects.filter(article_id = id).exists():
                        article = ArticleQuiz.objects.get(article_id = id)
                        title = article.article_title
                    titlelist.append([title,date])
                    if i ==2: break
            
        data ={
            'title': titlelist,
            'total_study': total_study,
            'avg_article_comprehension': avg_article_comprehension,
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
                for s in reversed(list(study)):
                    date = s.study_date.strftime("%Y-%m-%d %H:%M:%S")
                    step2_score = s.article_comprehension
                    step3_score = s.quiz_score
                    id = s.article_id
                    if ArticleQuiz.objects.filter(article_id = id).exists():
                        article = ArticleQuiz.objects.get(article_id = id)
                        title = article.article_title
                    titlelist.append([title,date,step2_score,step3_score])
            
        data ={
            'title': titlelist,
        }
        return JsonResponse(data)
    else :
            return JsonResponse(status=401, safe=False)