from datetime import datetime
from django.contrib import admin
from django.http import HttpResponse
from openpyxl import Workbook
import pytz
from django.utils import timezone
from .models import Countries, Location, Department, Doctor, Booking, Hospital


class CountryAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Countries model.
    """
    list_display = ('id', 'name')  


class LocationAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Location model.
    """
    list_display = ('id', 'name', 'country')  
    list_filter = ['country']


class DepartmentAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Department model.
    """
    list_display = ('id', 'name','location')  
    list_filter = ['location']


class DoctorAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Doctor model.
    """
    list_display = ('id', 'name', 'location', 'department', 'charge', 'start_time', 'end_time','slot','pic') 
    list_filter = ['start_time','end_time'] 

class TimeFilter(admin.SimpleListFilter):
    title = 'Booking Time'
    parameter_name = 'booking_time'

    def lookups(self, request, model_admin):
        return (
            ('morning', 'Morning (9AM - 12PM)'),
            ('afternoon', 'Afternoon (3PM - 8PM)'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'morning':
            return queryset.filter(booking_time__range=('09:00:00', '12:00:00'))
        elif self.value() == 'afternoon':
            return queryset.filter(booking_time__range=('15:00:00', '20:00:00'))
        
        
class BookingAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Booking model.
    """
    list_display = ('id', 'name', 'address', 'doctor','status','booking_time','user')  
    list_filter = [TimeFilter]
    actions = ['download_bookings']

    def convert_to_ist(self, booking_time):
        # Convert booking_time to IST
        """
        Convert booking time from UTC to Indian Standard Time (IST).

        Args:
            booking_time (datetime): The booking time in UTC.

        Returns:
            str: The booking time converted to IST in 'HH:MM' format.
        """

        railway_time = timezone.localtime(booking_time)
        ist = pytz.timezone('Asia/Kolkata')
        return railway_time.astimezone(ist).strftime('%H:%M')

    def download_bookings(self, request, queryset):
        """
        Download selected bookings as an Excel file.

        Args:
            request: The HTTP request object.
            queryset: A queryset containing the selected bookings.

        Returns:
            HttpResponse: An HTTP response with the Excel file attached.
        """
        
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename="bookings.xlsx"'

        wb = Workbook()
        ws = wb.active
        ws.append(['ID', 'Name', 'Address', 'Doctor', 'Status', 'Booking Time', 'User'])

        for booking in queryset:
            doctor_info = f"{booking.doctor.name} - ({booking.doctor.location}) - ({booking.doctor.department})"
            user_info = f"{booking.user.username}"
            ws.append([booking.id, booking.name, booking.address, doctor_info, booking.status, booking.booking_time, user_info])

        wb.save(response)
        return response

    download_bookings.short_description = "Download The Selected Booking Details"

    
class HospitalAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Hospital model.
    """
    list_display = ('id', 'name', 'country','location','address', 'contact_number', 'image')  
    list_filter = ['country','location']

# Registering admin classes
admin.site.register(Countries, CountryAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(Department, DepartmentAdmin)
admin.site.register(Doctor, DoctorAdmin)
admin.site.register(Booking, BookingAdmin)
admin.site.register(Hospital, HospitalAdmin)
