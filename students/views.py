from django.http import HttpResponse
from rest_framework import viewsets
from .models import Student
from .serializer import StudentSerializer
from django.shortcuts import render

class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

def home(request):
    return render(request, 'resume.html')
