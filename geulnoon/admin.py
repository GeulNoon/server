from django.contrib import admin

from .models import User, ArticleQuiz

class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'nickname', 'password', 'birthyear')

class ArticleQuizAdmin(admin.ModelAdmin):
    list_display = ('article_id', 'article_count', 'article_content', 'article_title', 'article_summary', 'quiz1_content', 'quiz2_content', 'quiz3_content', 'quiz4_content', 'quiz1_answer', 'quiz2_answer', 'quiz3_answer', 'quiz4_answer', 'email')

admin.site.register(User, UserAdmin)
admin.site.register(ArticleQuiz, ArticleQuizAdmin)
