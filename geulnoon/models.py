from django.db import models


class User(models.Model):
    email = models.CharField(primary_key=True, max_length=45)
    nickname = models.CharField(max_length=30)
    password = models.CharField(max_length=60)
    birthyear = models.TextField()  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'user'