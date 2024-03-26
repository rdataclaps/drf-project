from django.http import HttpResponse, JsonResponse
from rest_framework import viewsets
from .models import Student, Teacher
from .serializer import StudentSerializer
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status


class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

    def create(self, request, *args, **kwargs):
        '''By this function we will be able to add new student.'''
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    


def get_teacher(request):
    teachers = Teacher.objects.filter(name="Deepak")
    teacher_data = [{'id': teacher.id, 'name': teacher.name, 'Subject':teacher.Subject} for teacher in teachers]
    return JsonResponse({'teachers': teacher_data})


    
def home(request):
    return render(request, 'resume.html')


def student(request):
    students=Student.objects.filter().order_by('name')
    return render(request, 'students.html', {'students':students})

