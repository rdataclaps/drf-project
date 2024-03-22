# urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'students-info', views.StudentViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('home/',views.home, name='home'),
    path('student/',views.student, name='student'),
    path('teachers/',views.get_teacher, name='teachers'),
]
