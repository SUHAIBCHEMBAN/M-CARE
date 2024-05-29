import random
from constants import *
from .forms import ProfileForm
from .models import UserProfile
from django.core.mail import send_mail
from django.http import JsonResponse
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render ,get_object_or_404
from django.contrib.auth import get_user_model, login as auth_login, logout


# this my user_login views function
@never_cache
def user_login(request):
    """
    View function for user login.

    If the user is already authenticated, redirect to the booking page.
    If the request method is POST, check if the user with the provided email exists.
    If the user exists, send an OTP and redirect to OTP verification page.
    If the user doesn't exist, create a new user and redirect to OTP verification page.
    """
    if request.user.is_authenticated:
        return redirect('booking')
    
    if request.method == 'POST':
        email = request.POST.get('email')
        request.session['email'] = email
        username = request.POST.get('username')

        
        # New 
        User = get_user_model()
        
        if User.objects.filter(username=username).exists():
            error_message = USERNAME_ERROR
            return render(request, 'login.html', {'error_message': error_message})
        
        user = get_user_model().objects.filter(email=email).first()
        if user:
            otp = ''.join(random.choices('0123456789', k=6))
            request.session['otp'] = otp
            mail_subject = 'M-CARE HOSPITAL'
            message = f'Your OTP is: {otp}'
            send_mail(mail_subject, message, 'your_email@example.com', [email])
            return redirect('verify_otp')          
        else:   
            user = get_user_model().objects.create_user(username=username, email=email)
            return redirect('verify_otp')

    return render(request, 'login.html')


# this my verify_otp views function
@never_cache
def verify_otp(request):
    """
    View function for OTP verification.

    If the OTP is not in session, redirect to the login page.
    If the request method is POST, verify the entered OTP.
    If the OTP matches, authenticate the user and redirect to the booking page.
    If the OTP doesn't match, render the OTP verification page with an error message.
    """
    if 'otp' not in request.session:
        # OTP not generated, redirect to login
        return redirect('login')
    
    if request.method == 'POST':
        # Get entered OTP
        entered_otp = request.POST.get('otp')
        # Get stored OTP from session
        stored_otp = request.session.get('otp')
        
        if entered_otp == stored_otp:
            # OTP matched, remove OTP from session
            del request.session['otp']
            # Authenticate and login user
            email = request.session.get('email')
            user = get_object_or_404(get_user_model(), email=email)
            auth_login(request, user)

            # Set session variable to indicate booking success
            request.session['booking_success'] = True
            
            message = "Your Login Successfully Completed"
            return render(request,'home.html',{'message':message})
           
        else:
            # OTP didn't match, render OTP verification page with error
            return render(request, 'otp_verification.html', {'error': 'Invalid OTP'})
    
    return render(request, 'otp_verification.html')


# this my status changing views.py function 
def clear_booking_success(request):
    """
    Clears the 'booking_success' key from the session if it exists.

    Args:
        request: The HTTP request object.

    Returns:
        A JSON response with a status of 'success' after removing the 'booking_success' key from the session.
    """
    if 'booking_success' in request.session:
        del request.session['booking_success']
    return JsonResponse({'status': 'success'})


# this my user_logout views function
@never_cache
def user_logout(request):
    """
    View function for user logout.

    If the user is authenticated, logout and redirect to the home page.
    """
    if request.user.is_authenticated:
        logout(request)
    return redirect('home')


# this add another account function
def add_login(request):
    """
    Log out the user if authenticated, otherwise redirect to login page.

    Args:
        request: HTTP request object.

    Returns:
        Redirect to the login page.
    """
    if request.user.is_authenticated:
        logout(request)
        return redirect('login')
    return redirect('login')


# this login success page render function
# def login_success(request):
#     """
#     Render function for the login success page.

#     Parameters:
#     - request: The HTTP request object.

#     Returns:
#     - Renders the success.html template.
#     """
#     return render(request,'success.html')


# this my user profile views function
def profile(request):
    """
    Render function for the user profile page.

    If the user is authenticated, the function retrieves the user's profile information.
    If the request method is POST, it handles profile picture uploads and username updates.
    Renders the profile.html template with the profile form and user information.

    Parameters:
    - request: The HTTP request object.

    Returns:
    - Renders the profile.html template with the profile form and user information.
    """
    if request.user.is_authenticated:
        try:
            profile_instance = request.user.userprofile
        except UserProfile.DoesNotExist:
            profile_instance = UserProfile(user=request.user)
            profile_instance.save()

        if request.method == 'POST':
            if 'profile_picture' in request.FILES:  # Check if profile picture is being uploaded
                form = ProfileForm(request.POST, request.FILES, instance=profile_instance)
                if form.is_valid():
                    form.save()
            elif 'username' in request.POST:  # Check if username is being updated
                new_username = request.POST['username']
                request.user.username = new_username
                request.user.save()
            return redirect('profile')
        else:
            form = ProfileForm(instance=profile_instance)
        return render(request, 'profile.html', {'form': form, 'user': request.user})
    else:
        return render(request, 'profile.html')


