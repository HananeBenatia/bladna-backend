from django.db import models
from django.contrib.auth.models import AbstractUser 

class User (AbstractUser) :                                                # Create your models here.
    full_name = models.CharField (max_length=100, blank=True)
    age = models.PositiveIntegerField ()
    username = models.CharField (max_length=150, unique=True)
    password = models.CharField(max_length=100)
    parent_secret= models.CharField(max_length=100, blank=True, null=True)
    score = models.PositiveIntegerField (default=0)
    region_choices = [
        ('South' , 'south') ,
        ('East' , 'east') ,
        ('Center' , 'center') ,
        ('Ouest' , 'ouest') ,
    ]
    region = models.CharField(max_length=10, choices=region_choices, blank=True, default = 'south')
    def __str__(self):
        return self.username

class Progress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="progresses")
    region = models.CharField(max_length=10, choices=User.region_choices)
    score = models.PositiveIntegerField()
    play_date = models.DateField()

    def __str__(self):
        return f"{self.user.username} - {self.play_date}"