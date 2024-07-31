from celery import shared_task
from datetime import timedelta
from django.utils.timezone import now
from .models import Booking

@shared_task
def check_bookings():
    expired_time = now() - timedelta(days=1) 
    bookings = Booking.objects.filter(status='Success', booking_date__lt=expired_time.date())
    for booking in bookings:
        booking.status = 'Expired'
        booking.save(update_fields=['status'])
        print('Celery Is Done')
