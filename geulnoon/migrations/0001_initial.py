# Generated by Django 4.0.2 on 2022-03-10 23:03

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ArticleQuiz',
            fields=[
                ('article_id', models.IntegerField(primary_key=True, serialize=False)),
                ('article_count', models.IntegerField()),
                ('article_content', models.CharField(max_length=10000)),
                ('article_title', models.CharField(max_length=200)),
                ('article_summary', models.JSONField()),
                ('quiz1_content', models.JSONField()),
                ('quiz2_content', models.JSONField()),
                ('quiz3_content', models.JSONField()),
                ('quiz4_content', models.JSONField()),
                ('quiz1_answer', models.CharField(max_length=30)),
                ('quiz2_answer', models.CharField(max_length=30)),
                ('quiz3_answer', models.CharField(max_length=30)),
                ('quiz4_answer', models.CharField(max_length=30)),
            ],
            options={
                'db_table': 'article_quiz',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Study',
            fields=[
                ('study_id', models.IntegerField(primary_key=True, serialize=False)),
                ('study_date', models.DateTimeField()),
                ('study_type', models.IntegerField()),
                ('user_summary', models.CharField(blank=True, max_length=2000, null=True)),
                ('quiz_count', models.IntegerField()),
                ('quiz1_user_answer', models.CharField(blank=True, max_length=30, null=True)),
                ('quiz2_user_answer', models.CharField(blank=True, max_length=30, null=True)),
                ('quiz3_user_answer', models.CharField(blank=True, max_length=30, null=True)),
                ('quiz4_user_answer', models.CharField(blank=True, max_length=30, null=True)),
                ('quiz1_user_answer_correct', models.IntegerField()),
                ('quiz2_user_answer_correct', models.IntegerField()),
                ('quiz3_user_answer_correct', models.IntegerField()),
                ('quiz4_user_answer_correct', models.IntegerField()),
                ('article_comprehension', models.FloatField()),
                ('quiz_score', models.IntegerField()),
                ('email', models.CharField(max_length=45)),
                ('article_id', models.IntegerField()),
            ],
            options={
                'db_table': 'study',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('email', models.CharField(max_length=45, primary_key=True, serialize=False)),
                ('nickname', models.CharField(max_length=30)),
                ('password', models.CharField(max_length=60)),
                ('birthyear', models.TextField()),
            ],
            options={
                'db_table': 'user',
                'managed': False,
            },
        ),
    ]
