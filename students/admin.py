from django.contrib import admin
from .models import Student, Teacher
# Register your models here.

@admin.register(Student)
class StudentModel(admin.ModelAdmin):
    list_display = ['id', 'name', 'roll', 'city']

@admin.register(Teacher)
class TeacherModel(admin.ModelAdmin):
    list_display = ['id', 'name', 'subject', 'joining_date']
