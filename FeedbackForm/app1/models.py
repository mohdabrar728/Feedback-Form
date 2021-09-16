from django.db import models


# Create your models here.


class TempModel(models.Model):
    question = models.CharField(max_length=255)
    type = models.CharField(max_length=255)
    options = models.TextField(null=True)


class FormTokenModel(models.Model):
    form_name = models.CharField(max_length=100)
    form_token = models.CharField(max_length=100)
    form_code = models.TextField()
    form_unmask = models.BooleanField()


class EmailTokenModel(models.Model):
    form_token = models.CharField(max_length=100)
    email_id = models.EmailField(max_length=100)
    email_token = models.CharField(max_length=100)
