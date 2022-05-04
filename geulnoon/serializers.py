from rest_framework import serializers
from .models import User, ArticleQuiz, Study

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'email',
            'nickname',
            'password',
            'birthyear',
        )
        model = User


class ArticleQuizSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'article_id',
            'article_count',
            'article_content',
            'article_title',
            'article_summary',
            'article_keyword',#4.30추가
            'quiz1_content'
            'quiz2_content',
            'quiz3_content',
            'quiz4_content',
            'quiz1_answer',
            'quiz2_answer',
            'quiz3_answer',
            'quiz4_answer',
            'email'
        )
        model = ArticleQuiz

class StudySerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'study_id',
            'study_date',
            'study_type',
            'choice',
            'user_summary',
            'quiz_count',
            'quiz1_user_answer',
            'quiz2_user_answer',
            'quiz3_user_answer ',
            'quiz4_user_answer',
            'quiz1_user_answer_correct',
            'quiz2_user_answer_correct ',
            'quiz3_user_answer_correct',
            'quiz4_user_answer_correct',
            'article_comprehension',
            'quiz_score',
            'keyword_user_answer',#4.30추가
            'keyword_score',#4.30추가
            'issubmitted',
            'email',
            'article_id',
        )
        model = Study