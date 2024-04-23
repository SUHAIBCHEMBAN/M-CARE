from django.contrib import admin
from .models import Doctor,Booking,Hospital

class DoctorAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Doctor model.
    """
    list_display = ('id', 'name', 'location', 'department', 'charge', 'start_time', 'end_time')

admin.site.register(Doctor, DoctorAdmin)

class BookingAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Booking model.
    """
    list_display = ('id', 'name', 'address', 'doctor', 'booking_time')

admin.site.register(Booking, BookingAdmin)

class HospitalAdmin(admin.ModelAdmin):
    list_display = ('id','title','city','street','state')
admin.site.register(Hospital,HospitalAdmin)

