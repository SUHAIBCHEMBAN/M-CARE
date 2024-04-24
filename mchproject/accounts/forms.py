from django import forms
from .models import MyUser

class UserRegistrationForm(forms.ModelForm):
    """
    User registration form.

    Allows users to register with a username and email.
    """

    class Meta:
        model = MyUser
        fields = ['username', 'email']
        
class OTPForm(forms.Form):
    """
    OTP verification form.

    Allows users to enter the OTP sent to their email for verification.
    """

    otp = forms.CharField(max_length=6)