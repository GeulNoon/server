import email
from http.client import HTTPResponse
from pickle import FALSE
from urllib import response
from django.shortcuts import render
from rest_framework import generics
import json
from django.http import JsonResponse, HttpResponse
from rest_framework.decorators import api_view
import bcrypt
import jwt  
from .key import SECRET_KEY, ALGORITHM

from .models import User
from .serializers import UserSerializer

class ListPost(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class DetailPost(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

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