from django.db import models
from django.contrib.auth.models import AbstractUser 

class User (AbstractUser) :                                                # Create your models here.
    full_name = models.CharField (max_length=100, blank=True)
    age = models.PositiveIntegerField ()
    username = models.CharField (max_length=150, unique=True)
    password = models.CharField(max_length=100)
    def __str__(self):
        return self.username
