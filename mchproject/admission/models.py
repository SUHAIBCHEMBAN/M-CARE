from django.db import models
from django.core.exceptions import ValidationError

class Course(models.Model):
    name = models.CharField(max_length=100)
    slots = models.PositiveIntegerField()

    def __str__(self):
        return self.name

    def has_available_slots(self):
        return self.student_set.count() < self.slots

class Student(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    email = models.EmailField()
    phone_number = models.CharField(max_length=15)
    address = models.TextField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def clean(self):
        if not self.course.has_available_slots():
            raise ValidationError(f"No slots available for the course: {self.course.name}")
