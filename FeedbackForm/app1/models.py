from django.db import models


# Create your models here.
class FormCreateModel(models.Model):
    title = models.CharField(max_length=100)


class TempModel(models.Model):
    question = models.CharField(max_length=255)
    type = models.CharField(max_length=255)
    options = models.TextField(null=True)
