from django.contrib import admin
from django.urls import path
from . import views


urlpatterns = [
   path('custom-admin/',views.admin_login, name='admin_login'),
   path('dashboard/', views.admin_dashboard, name='admin_dashboard'),
   path('logout/',views.admin_logout,name='logout'),
]