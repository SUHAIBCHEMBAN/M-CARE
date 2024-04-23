from django.contrib import admin

# Register your models here.

from .models import MyUser
class UserAdmin(admin.ModelAdmin):
    list_display = ('id','username','email','otp')
admin.site.register(MyUser,UserAdmin) 