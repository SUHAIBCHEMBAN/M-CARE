from django.contrib import admin

# Register your models here.

from .models import UserProfile
class CustomAdmin(admin.ModelAdmin):
    list_display = ('id','user')
admin.site.register(UserProfile,CustomAdmin) 