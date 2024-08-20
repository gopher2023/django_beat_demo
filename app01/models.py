from django.db import models


# Create your models here.

class Article(models.Model):
    title = models.CharField(max_length=64)
    url = models.CharField(max_length=64)
    author = models.CharField(max_length=64)
    desc = models.TextField()

# 迁移