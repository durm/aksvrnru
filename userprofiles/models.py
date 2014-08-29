#-*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, unique=True, verbose_name="Пользователь")
    phone = models.CharField(max_length=10, verbose_name="Телефон")