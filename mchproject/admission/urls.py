from django.urls import path
from . import views

urlpatterns = [
    path('admission/', views.student_admission, name='student_admission'),
    path('admission_details/',views.admission_details,name='admission_details'),
]
