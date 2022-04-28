# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class ArticleQuiz(models.Model):
    article_id = models.IntegerField(primary_key=True)
    article_count = models.IntegerField()
    article_content = models.CharField(max_length=10000)
    article_title = models.CharField(max_length=200)
    article_summary = models.JSONField()
    quiz1_content = models.JSONField()
    quiz2_content = models.JSONField()
    quiz3_content = models.JSONField()
    quiz4_content = models.JSONField()
    quiz1_answer = models.CharField(max_length=30)
    quiz2_answer = models.CharField(max_length=30)
    quiz3_answer = models.CharField(max_length=30)
    quiz4_answer = models.CharField(max_length=200)
    email = models.ForeignKey('User', models.DO_NOTHING, db_column='email')

    class Meta:
        managed = False
        db_table = 'article_quiz'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Study(models.Model):
    study_id = models.IntegerField(primary_key=True)
    study_date = models.DateTimeField()
    study_type = models.IntegerField()
    user_summary = models.CharField(max_length=2000, blank=True, null=True)
    quiz_count = models.IntegerField()
    quiz1_user_answer = models.CharField(max_length=30, blank=True, null=True)
    quiz2_user_answer = models.CharField(max_length=30, blank=True, null=True)
    quiz3_user_answer = models.CharField(max_length=30, blank=True, null=True)
    quiz4_user_answer = models.CharField(max_length=30, blank=True, null=True)
    quiz1_user_answer_correct = models.IntegerField()
    quiz2_user_answer_correct = models.IntegerField()
    quiz3_user_answer_correct = models.IntegerField()
    quiz4_user_answer_correct = models.IntegerField()
    article_comprehension = models.FloatField()
    quiz_score = models.IntegerField()
    field_issubmitted = models.IntegerField(db_column=' issubmitted')  # Field renamed to remove unsuitable characters. Field renamed because it started with '_'.
    email = models.ForeignKey('User', models.DO_NOTHING, db_column='email')
    article = models.ForeignKey(ArticleQuiz, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'study'


class User(models.Model):
    email = models.CharField(primary_key=True, max_length=45)
    nickname = models.CharField(max_length=30)
    password = models.CharField(max_length=60)
    birthyear = models.TextField()  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'user'
