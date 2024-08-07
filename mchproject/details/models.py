from django.db import models
from datetime import time
from datetime import timedelta
from django.utils import timezone
from django.contrib.auth.models import User


class Banner_Cards(models.Model):
    title = models.CharField(max_length=500,default='no title')
    image = models.ImageField(upload_to='homeimg',default='default_image.jpg') 

class Main_Cards(models.Model):
    crd_img = models.ImageField(upload_to='main_crd_img')
    title = models.CharField(max_length=50)
    discription = models.CharField(max_length=50)
    button = models.CharField(max_length=50)
    button_url = models.URLField(default='/doctor')

    def __str__(self) -> str:
        return self.title

class Location_Cards(models.Model):
    image = models.ImageField(upload_to='location_img',default='defualt_image.jpg')
    title = models.CharField(max_length=20)
    click_url = models.URLField(default='/indian')

    def __str__(self):
        return self.title

class Countries(models.Model):
    """
    Model representing countries.
    """
    name = models.CharField(max_length=100)  

    def __str__(self):
        """
        String for representing the Model object (country name).
        """
        return self.name


class Location(models.Model):
    """
    Model representing locations.
    """
    name = models.CharField(max_length=100)
    country = models.ForeignKey(Countries, on_delete=models.CASCADE)

    def __str__(self):
        """
        String for representing the Model object (location name and country).
        """
        return f"{self.name} - {self.country}"


class Department(models.Model):
    """
    Model representing departments.
    """
    name = models.CharField(max_length=100)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)

    def __str__(self):
        """
        String for representing the Model object (department name).
        """
        return self.name


class Doctor(models.Model):
    """
    Model representing doctors.
    """
    pic = models.ImageField(upload_to='docimg',default='default_image.jpg')
    name = models.CharField(max_length=100)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    charge = models.IntegerField(default=200)
    start_time = models.TimeField(default=time(hour=8))  
    end_time = models.TimeField(default=time(hour=12)) 
    slot = models.IntegerField(default=20) 

    def __str__(self):
        """
        String for representing the Model object (doctor name, department, and location).
        """
        return f"Dr {self.name} - ({self.department.name}) - ({self.location.name})"


class Booking(models.Model):
    """
    Model representing bookings.
    """
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=150)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    booking_date = models.DateField()
    booking_time = models.TimeField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    STATUS_CHOICES = (
        ('Pending','Pending'),
        ('Success','Success'),
        ('Visited','Visited'),
        ('Expired','Expired'),
    )
    status = models.CharField(max_length=50,choices=STATUS_CHOICES,default='Pending')


    def __str__(self):
        """
        String for representing the Model object (booking name, doctor name, and booking time).
        """
        return f"{self.name} - {self.doctor.name}"  


class Hospital(models.Model):
    """
    Model representing hospitals.
    """
    name = models.CharField(max_length=200)
    country = models.ForeignKey(Countries, on_delete=models.CASCADE)
    location = models.ForeignKey(Location,on_delete=models.CASCADE)
    address = models.TextField()
    contact_number = models.CharField(max_length=20)
    image = models.ImageField(upload_to='hospitals', default='default_image.jpg')

    def __str__(self):
        """
        String for representing the Model object (hospital name).
        """
        return self.name
