from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name='home'),
    path('finddoctor/',views.find_doctor,name='finddoctor'),
    path('appointment/',views.appointment,name='appointment'),
    path('booking/',views.booking,name='booking'),
    path('bookingsuccess/',views.booking_success,name='booking_success'),
    path('aboutus/',views.aboutus,name='aboutus'),
    path('bookingdetails/',views.booking_details,name='booking_details'),
    path('cancelbooking/<int:booking_id>/',views.cancel_booking,name='cancel_booking'),
    path('indian/',views.indian,name='indian'),
    path('uae/',views.uae,name='uae'),
    path('canada/',views.canada,name='canada'),
]   