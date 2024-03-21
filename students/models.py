from django.db import models

# Create your models here.
class Student(models.Model):
    name = models.CharField(max_length = 255, null=False)
    roll =  models.IntegerField()
    city = models.CharField(max_length =255)

class Teacher(models.Model):
    name = models.CharField(max_length = 255, null=False)
    Subject = models.CharField(max_length = 255, null=False)
    joining_date =  models.DateField()
