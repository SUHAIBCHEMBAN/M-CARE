from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.user_login, name='login'),
    path('verify/', views.verify_otp, name='verify_otp'),
    path('logout/', views.user_logout,name='logout'),
    path('profile/',views.profile,name='profile'),
    path('addlogin/',views.add_login,name='add_login'),
    # path('success/',views.login_success,name='success'),
    path('clear-booking-success/', views.clear_booking_success, name='clear_booking_success'),
]
