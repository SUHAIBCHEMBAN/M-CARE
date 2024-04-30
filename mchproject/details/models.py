from django.db import models
from datetime import time

class Countries(models.Model):
    name = models.CharField(max_length=100)  

    def __str__(self):
        return self.name


class Location(models.Model):
    name = models.CharField(max_length=100)
    country = models.ForeignKey(Countries, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} - {self.country}"


class Department(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Doctor(models.Model):
    name = models.CharField(max_length=100)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    charge = models.IntegerField(default=200)
    start_time = models.TimeField(default=time(hour=8))  
    end_time = models.TimeField(default=time(hour=12))  

    def __str__(self):
        return f"Dr {self.name} - ({self.department.name}) - ({self.location.name})"


class Booking(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=150)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    booking_time = models.TimeField(verbose_name="Booking Time")

    def __str__(self):
        return f"{self.name} - {self.doctor.name} - {self.booking_time}"  


class Hospital(models.Model):
    name = models.CharField(max_length=200)
    country = models.ForeignKey(Countries, on_delete=models.CASCADE)
    address = models.TextField()
    contact_number = models.CharField(max_length=20)
    image = models.ImageField(upload_to='hospitals', default='default_image.jpg')

    def __str__(self):
        return self.name
