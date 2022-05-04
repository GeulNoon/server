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
    path('Step3/', views.step3),#5.01추가
    path('Step4/', views.step4),
    path('Step5/', views.step5),#4.30추가
    path('MyPage/', views.Mypage),
    path('searchWord/', views.searchWord),
    path('getAnswer/', views.getAnswer),
    path('getHistory/', views.GetHistory),
    path('getStatistics/', views.GetStatistics),
    path('getMoreHistory/', views.GetMoreHistory),
    path('reviewStudy/', views.ReviewStudy),#5.03 추가
]