import random
from django.shortcuts import redirect, render
from django.contrib.auth import get_user_model, login as auth_login, logout
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404

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
            
            # Redirect to success page
            return redirect('booking')
        else:
            # OTP didn't match, render OTP verification page with error
            return render(request, 'otp_verification.html', {'error': 'Invalid OTP'})
    
    return render(request, 'otp_verification.html')


def user_logout(request):
    """
    View function for user logout.

    If the user is authenticated, logout and redirect to the home page.
    """
    if request.user.is_authenticated:
        logout(request)
    return redirect('home')
