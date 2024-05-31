from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name='home'),
    path('finddoctor/',views.find_doctor,name='finddoctor'),
    path('doctors/',views.doctors,name='doctors'),  
    path('booking/',views.booking,name='booking'),
    path('aboutus/',views.aboutus,name='aboutus'),
    path('bookingdetails/',views.booking_details,name='booking_details'),
    path('cancelbooking/<int:booking_id>/',views.cancel_booking,name='cancel_booking'),
    path('save_doctor/<int:doctor_id>/', views.save_doctor, name='save_doctor'),
    path('saved_doctors/', views.saved_doctors, name='saved_doctors'),
    path('indian/',views.indian,name='indian'),
    path('uae/',views.uae,name='uae'),
    path('canada/',views.canada,name='canada'),
    path('api/departments/<int:location_id>/', views.get_departments_for_location, name='get_departments_for_location'),
]   
