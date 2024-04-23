from django.db import models


# Create your models here.

class Doctor(models.Model):

    """
    Model representing a doctor.

    """
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    charge = models.IntegerField(default=200)    
    start_time = models.TimeField(default='08:00')
    end_time = models.TimeField(default='12:00')
    

    def __str__(self):

        """
        Return a string representation of the doctor.
        """
        return 'Dr ' + self.name + ' - (' + self.department + ')' + ' - (' + self.location + ')'
    

class Booking(models.Model):

    """
    Model represending  a Booking
    """

    
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=150)
    doctor = models.ForeignKey(Doctor,on_delete=models.CASCADE)
    booking_time = models.TimeField(verbose_name="Booking Time")

    def __str__(self):
        
        """
        Return a string representation of the booking
        """
        return self.name 

class Hospital(models.Model):
    title = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    street = models.CharField(max_length=100)
    state = models.CharField(max_length=100)

    def __str__(self):
        return self.title