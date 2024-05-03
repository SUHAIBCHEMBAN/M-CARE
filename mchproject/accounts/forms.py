from django import forms
from .models import UserProfile

class ProfileForm(forms.ModelForm):
    """
    Form for updating user profile information.

    This form allows users to update their profile picture.

    Attributes:
    - profile_picture (ImageField): Field for uploading profile pictures.
    """
    class Meta:
        """
        Metadata class for the ProfileForm.

        Attributes:
        - model (UserProfile): The UserProfile model to use for the form.
        - fields (list): The fields of the UserProfile model to include in the form.
        """
        model = UserProfile
        fields = ['profile_picture']
