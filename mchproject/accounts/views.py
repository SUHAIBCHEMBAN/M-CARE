from django.shortcuts import render, redirect
from django.contrib.auth import login
from .models import MyUser
from .forms import UserRegistrationForm, OTPForm
from django.core.mail import send_mail
import random
from django.views.decorators.cache import never_cache



@never_cache
def user_login(request):
    """
    login view.

    Handles user registration and sends OTP to the user's email for verification.
    
    Parameters:
    - request: The HTTP request object.
    
    Returns:
    - If the form is valid, redirects to verify_otp page.
    - Otherwise, renders the signup page template with the form.
    """
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            # Generate OTP
            otp = ''.join([str(random.randint(0, 9)) for _ in range(6)])
            user.otp = otp
            user.save()
          
            
            # Send OTP to user's email
            send_mail(
                'M-CARE HOSPITAL',
                f'Your OTP is: {otp}',
                'your_email@example.com',
                [user.email],
                fail_silently=False,
            )
            return redirect('verify_otp', user_id=user.id)
    else:
        form = UserRegistrationForm()
    return render(request, 'user_login.html', {'form': form})

@never_cache
def verify_otp(request, user_id):
    """
    Verify OTP view.

    Verifies the OTP entered by the user.
    
    Parameters:
    - request: The HTTP request object.
    - user_id: The ID of the user.
    
    Returns:
    - If the OTP is correct, logs in the user and renders the home page.
    - Otherwise, renders the verify OTP page with the form.
    """
    user = MyUser.objects.get(id=user_id)
    if request.method == 'POST':
        form = OTPForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['otp'] == user.otp:
                user.is_verified = True
                user.save()
                login(request, user)
                return render(request, 'home.html')
            else:
                return render(request, 'home.html', {'form': form})
    else:
        form = OTPForm()
    return render(request, 'verify_otp.html', {'form': form})