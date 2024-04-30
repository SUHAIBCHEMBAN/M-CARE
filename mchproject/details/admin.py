from django.contrib import admin
from .models import Countries, Location, Department, Doctor, Booking, Hospital


class CountryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')  


class LocationAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'country')  


class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')  


class DoctorAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Doctor model.
    """
    list_display = ('id', 'name', 'location', 'department', 'charge', 'start_time', 'end_time')  


class BookingAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Booking model.
    """
    list_display = ('id', 'name', 'address', 'doctor', 'booking_time')  


class HospitalAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'country', 'address', 'contact_number', 'image')  
    

# Registering admin classes
admin.site.register(Countries, CountryAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(Department, DepartmentAdmin)
admin.site.register(Doctor, DoctorAdmin)
admin.site.register(Booking, BookingAdmin)
admin.site.register(Hospital, HospitalAdmin)
