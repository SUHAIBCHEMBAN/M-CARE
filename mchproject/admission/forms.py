from django import forms
from .models import Student

class StudentForm(forms.ModelForm):
    """
    Form for creating or updating a Student.
    """
    class Meta:
        model = Student
        fields = ['first_name', 'last_name', 'date_of_birth', 'email', 'phone_number', 'address', 'course']
