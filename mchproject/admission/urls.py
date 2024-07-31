from django.urls import path
from . import views

urlpatterns = [
    path('admission/', views.student_admission, name='student_admission'),
    path('admission_success/', views.student_admission_success, name='student_admission_success'),
]
