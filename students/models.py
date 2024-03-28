from django.db import models

# Create your models here.
class Student(models.Model):
    name = models.CharField(max_length = 255, null=False)
    roll =  models.IntegerField()
    city = models.CharField(max_length =255)

    def __str__(self):
        return f"{self.name}"

class Teacher(models.Model):
    name = models.CharField(max_length = 255, null=False)
    subject = models.CharField(max_length = 255, null=False)
    joining_date =  models.DateField()

    def __str__(self):
        return f"{self.name}"
