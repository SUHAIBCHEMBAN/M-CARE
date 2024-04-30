from django.urls import path
from .views import user_login, verify_otp,user_logout

urlpatterns = [
    path('login/', user_login, name='login'),
    path('verify/', verify_otp, name='verify_otp'),
    path('logout/', user_logout,name='logout'),
]
