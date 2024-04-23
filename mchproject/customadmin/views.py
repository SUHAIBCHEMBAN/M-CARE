from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import AdminLoginForm
from django.views.decorators.cache import never_cache

@never_cache
def admin_login(request):
    """
    Admin login function.

    This view handles the authentication of administrators.
    
    Parameters:
    - request: The HTTP request object.
    
    Returns:
    - If the request method is POST and the form is valid, redirects to admin_dashboard.
    - Otherwise, renders the login form template.
    """
    if request.method == 'POST':
        form = AdminLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None and user.is_superuser:
                login(request, user)
                return redirect('admin_dashboard')
    else:
        form = AdminLoginForm()

    return render(request, 'admin_login.html', {'form': form})

@never_cache
def admin_dashboard(request):
    """
    Admin dashboard view.

    This view renders the admin dashboard template.
    
    Parameters:
    - request: The HTTP request object.
    
    Returns:
    - Renders the admin dashboard template.
    """
    return render(request, 'dashboard.html')

@never_cache
def admin_logout(request):
    """
    Admin logout function.

    This view logs out the currently logged-in admin user and redirects to the login page.
    
    Parameters:
    - request: The HTTP request object.
    
    Returns:
    - Redirects to the login page.
    """
    logout(request)
    return redirect('user_login')
