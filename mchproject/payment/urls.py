from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('bookingsuccess/',views.booking_success,name='booking_success'),
    path('doctor_payment/',views.doctor_payment,name='payment_page'),
]