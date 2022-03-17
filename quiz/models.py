from django.conf import settings
from django.db import models
from django.utils import timezone


class Dated(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class User(Dated):
    name = models.CharField(max_length=256)
    last_name = models.CharField(max_length=256)
    phone_number = models.CharField(max_length=16)
    birthday = models.DateField(null=True)
    telegram_id = models.IntegerField(unique=True)  # правда ли id должен быть целочисленным
    telegram_login = models.CharField(max_length=256)
    referral = models.ForeignKey('self', on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.name


class Question(Dated):
    text = models.TextField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    photo = models.ImageField(blank=True, null=True)
    video = models.FileField(blank=True, null=True)
    sound = models.FileField(blank=True, null=True)

    def __str__(self):
        return self.text


class Answer(models.Model):
    question = models.ForeignKey(Question, related_name="answer", on_delete=models.CASCADE)
    answer = models.CharField(max_length=256)
    is_correct = models.BooleanField(default=True)


class Survey(Dated):
    title = models.CharField(max_length=256)
    description = models.TextField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    questions = models.ManyToManyField(Question, blank=True)
    is_published = models.BooleanField(default=False)

    def __str__(self):
        return self.title
