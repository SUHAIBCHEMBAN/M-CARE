from django.shortcuts import render,redirect
from django.views.decorators.cache import never_cache
# Create your views here.







# this success message veiws.py function
@never_cache
def booking_success(request):
    """
    View to render the booking success page.

    Renders the 'booking_success.html' template.

    Args:
        request (HttpRequest): The request object.

    Returns:
        HttpResponse: Rendered HTML template for booking success.
    """
    return render(request, 'booking_success.html')