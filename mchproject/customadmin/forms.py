from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate

class AdminLoginForm(AuthenticationForm):
    """
    Admin login form.

    This form extends Django's AuthenticationForm to add additional validation.
    """

    def clean(self):
        """
        Custom form validation.

        Validates the username and password and checks if the user is active.

        Returns:
        - cleaned_data: The cleaned form data.
        
        Raises:
        - ValidationError: If the username or password is missing, or if the user is invalid or inactive.
        """
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        if not username:
            raise forms.ValidationError("Please enter your username")
        if not password:
            raise forms.ValidationError("Please enter your password")

        user = authenticate(username=username, password=password)
        if user is None:
            raise forms.ValidationError("Invalid username or password")
        elif not user.is_active:
            raise forms.ValidationError("This account is inactive")

        return cleaned_data
