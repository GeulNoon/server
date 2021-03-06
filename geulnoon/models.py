from tkinter import CASCADE
from django.db import models

class User(models.Model):
    email = models.CharField(primary_key=True, max_length=45)
    nickname = models.CharField(max_length=30)
    password = models.CharField(max_length=60)
    birthyear = models.TextField()  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'user'

class ArticleQuiz(models.Model):
    article_id = models.IntegerField(primary_key=True)
    article_count = models.IntegerField()
    article_content = models.CharField(max_length=10000)
    article_title = models.CharField(max_length=200)
    article_summary = models.JSONField()
    article_keyword = models.CharField(max_length=10000) #4.30추가
    quiz1_content = models.JSONField()
    quiz2_content = models.JSONField()
    quiz3_content = models.JSONField()
    quiz4_content = models.JSONField()
    quiz1_answer = models.CharField(max_length=30)#05.03 길이 변경
    quiz2_answer = models.CharField(max_length=400)#05.03 길이 변경
    quiz3_answer = models.CharField(max_length=400)#05.03 길이 변경
    quiz4_answer = models.CharField(max_length=30)#05.03 길이 변경
    email = models.ForeignKey('User', models.DO_NOTHING, db_column='email')


    class Meta:
        managed = False
        db_table = 'article_quiz'

class Study(models.Model):
    study_id = models.IntegerField(primary_key=True)
    study_date = models.DateTimeField()
    study_type = models.IntegerField()
    choice = models.JSONField()
    user_summary = models.CharField(max_length=2000, blank=True, null=True)
    quiz_count = models.IntegerField()
    quiz1_user_answer = models.CharField(max_length=30, blank=True, null=True)
    quiz2_user_answer = models.CharField(max_length=400, blank=True, null=True)
    quiz3_user_answer = models.CharField(max_length=400, blank=True, null=True)
    quiz4_user_answer = models.CharField(max_length=30, blank=True, null=True)
    quiz1_user_answer_correct = models.IntegerField()
    quiz2_user_answer_correct = models.CharField(max_length=30)
    quiz3_user_answer_correct = models.CharField(max_length=30)
    quiz4_user_answer_correct = models.IntegerField()
    article_comprehension = models.FloatField()
    quiz_score = models.IntegerField()
    keyword_user_answer = models.JSONField()#4.30추가
    keyword_score = models.FloatField()#4.30추가
    issubmitted = models.BooleanField(default = False)
    email = models.CharField(max_length=45)
    article_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'study'