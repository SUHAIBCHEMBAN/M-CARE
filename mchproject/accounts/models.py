from django.contrib.auth.models import User
from django.db import models
from details.models import Doctor

class UserProfile(models.Model):
    """
    Model representing user profile information.

    This model extends the built-in User model provided by Django and
    stores additional information such as profile picture.

    Attributes:
    - user (OneToOneField): Reference to the associated user.
    - profile_picture (ImageField): Profile picture of the user.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pics', blank=True, null=True)
    saved_doctors = models.ManyToManyField(Doctor, related_name='saved_by_users')

