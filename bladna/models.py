from django.db import models
from django.contrib.auth.models import AbstractUser 

class User (AbstractUser) :                                                # Create your models here.
    full_name = models.CharField (max_length=100, blank=True)
    age = models.PositiveIntegerField ()
    username = models.CharField (max_length=150, unique=True)
    password = models.CharField(max_length=100)
    parent_secret= models.CharField(max_length=100, blank=True, null=True)
    def __str__(self):
        return self.username


'''class Parent ( models.Model ) : 
    user = models.OneToOneField( User , on_delete= models.CASCADE , related_name= 'parent')
    secret_answer = models.CharField(max_length=100)
    def __str__(self):
        return self.secret_answer'''