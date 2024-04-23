from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    """
    User profile model.

    Represents additional information associated with a user.
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    