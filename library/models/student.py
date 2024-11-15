from django.db import models
from django.utils import timezone

class Student(models.Model):
    RA = models.CharField(max_length=9, primary_key=True)
    RG = models.CharField(max_length=6, unique=True)
    name = models.CharField(max_length=50, unique=False)
    birthday = models.DateField()