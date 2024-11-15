from django.db import models
from django.utils import timezone

class Student(models.Model):
    RA = models.CharField(max_length=6, primary_key=True)
    RG = models.CharField(max_length=9, unique=True, null=False)
    name = models.CharField(max_length=50, unique=False, null=False)
    birthday = models.DateField(null=False)