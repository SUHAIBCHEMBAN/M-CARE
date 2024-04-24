from django.shortcuts import render, redirect
from django.contrib.auth import login
from .models import MyUser
from .forms import UserRegistrationForm,OTPForm
from django.core.mail import send_mail
import random




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
    user = None 

    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            existing_user = MyUser.objects.filter(email=email).first()
            if existing_user:
                otp = ''.join([str(random.randint(0,9)) for _ in range(6)])
                existing_user.otp = otp
                existing_user.save()
                send_mail(
                    'M-CARE HOSPITAL',
                    f'Your OTP is: {otp}',
                    'your_email@example.com',
                    [existing_user.email],
                    fail_silently=False,
                )
            else:
                user = form.save(commit=False)
                otp = ''.join([str(random.randint(0,9)) for _ in range(6)])
                user.otp = otp
                user.save()

                if user:
                    # Send OTP to user's email
                    send_mail(
                        'M-CARE HOSPITAL',
                        f'Your OTP is: {otp}',
                        'your_email@example.com',
                        [user.email],
                        fail_silently=False,
                    )
            return redirect('verify_otp',user_id=existing_user.id if existing_user else user.id)
    else:
        form = UserRegistrationForm()
    return render(request, 'user_login.html', {'form': form})



    
def verify_otp(request, user_id):
    """
    Verify OTP view.

    Verifies the OTP entered by the user.
    
    Parameters:
    - request: The HTTP request object.
    - user_id: The ID of the user.
    
    Returns:
    - If the OTP is correct, logs in the user and renders the booking page.
    - Otherwise, renders the verify OTP page with the form.
    """
    try:
        user = MyUser.objects.get(id=user_id)
    except MyUser.DoesNotExist:
        return redirect('home')  # Redirect to home page if user does not exist

    if request.method == 'POST':
        form = OTPForm(request.POST)
        if form.is_valid():
            otp_entered = form.cleaned_data['otp']
            if otp_entered == user.otp:
                user.is_verified = True
                user.save()
                login(request, user)
                return redirect('booking')  # Redirect to booking page after successful OTP verification
    else:
        form = OTPForm()

    return render(request, 'verify_otp.html', {'form': form})

