from django.urls import path

from . import views

urlpatterns = [
    path('', views.ListPost.as_view()),
    path('<int:pk>/', views.DetailPost.as_view()),
    path('signup', views.SignUp),
    path('login', views.LogIn),
    path('study', views.EnterArticle),
    path('title/', views.title),
    path('Step1/', views.step1),
    path('Step2/', views.step2),
    path('Step4/', views.step4),
    path('MyPage/', views.Mypage),
    path('searchWord/', views.searchWord),
    path('getAnswer/', views.getAnswer),
    path('getHistory/', views.GetHistory),
    path('getMoreHistory/', views.GetMoreHistory),
]
