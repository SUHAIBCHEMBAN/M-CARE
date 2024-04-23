from django.db import models

# # Create your models here.

class MyUser(models.Model):

    """
    User model.

    Represents a user in the system.
    
    """
      
    username = models.CharField(max_length=10)
    email = models.EmailField(unique=False)
    otp = models.CharField(max_length=6)

    def __str__(self):
        return self.username