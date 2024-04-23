from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.user_login, name='user_login'),
    path('verify_otp/<int:user_id>/', views.verify_otp, name='verify_otp'),
]   