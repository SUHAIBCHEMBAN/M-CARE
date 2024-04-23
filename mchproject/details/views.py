from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from datetime import datetime, time
from django.core.cache import cache
from .models import Doctor,Booking,Hospital


# Create your views here.

# @login_required
# this home views.py function
# @never_cache  
def home(request):
    """
    Home view.

    Renders the home page with the username of the logged-in user.
    
    Parameters:
    - request: The HTTP request object.
    
    Returns:
    - Renders the home page template with the username.
    """
    return render(request, 'home.html')



@never_cache
def find_doctor(request):   
    """
    View function to find doctors based on location and department.

    Retrieves doctors based on user-selected location and department,
    and renders them on the 'filtered_doctors.html' template. If no doctors
    match the selected criteria, it renders the same template with a message
    indicating no matching doctors found.

    Parameters:
    - request: HttpRequest object

    Returns:
    - Rendered HttpResponse object containing either the 'filtered_doctors.html' 
      template with the list of matching doctors or the 'finddoctor.html' template 
      with a form to select location and department.
    """

    # Initialize doctors variable
    doctors = None

    # Check if the request method is POST
    if request.method == 'POST':
        # Get location and department from POST data
        location = request.POST.get('location')
        department = request.POST.get('department')
        
       
        # Generate cache key based on location and department
        cache_key = f"doctors_{location}_{department}"
        
        # Check if data is cached
        doctors = cache.get(cache_key)
        
        
        # If data is not cached, retrieve it from the database
        if not doctors:
        
            doctors = Doctor.objects.filter(location=location, department=department)

            
            # Cache the data for 2 minutes
            cache.set(cache_key, doctors, timeout=120)
        
        # If no doctors found, render template with message
        if not doctors:
            message = "Sorry, No Doctors Available The Selected Criteria"
            return render(request, 'filtered_doctors.html', {'message': message})
        
        # Render template with list of doctors
        return render(request, 'filtered_doctors.html', {'doctors': doctors})
    
    # If request method is not POST, populate context with locations and departments
    context = {
        'locations': Doctor.objects.values_list('location', flat=True).distinct(),  
        'departments': Doctor.objects.values_list('department', flat=True).distinct()  
    }
    
    # Render template with context
    return render(request, 'finddoctor.html', context)


# this user appointment views.py function
@never_cache
def appointment(request):
    """
    appointment view.

    Render the appointment page.

    Parameters:

    - request: The HTTP request object.

    Returns:

    - Renders the find appointment page template.

    """
    return render(request,'appointment.html')



# this user booking views.py function
@never_cache
def booking(request):
    """
    View function to handle the booking process.

    POST method:
        Validates user input for name, address, doctor, and booking time.
        Checks if the selected time is within the doctor's working hours.
        Verifies if the selected time slot is available for booking with the chosen doctor.
        Ensures that the doctor has available slots for booking (up to a maximum of 5 bookings).
        Creates the booking if all validations pass.

    GET method:
        Retrieves all doctors for displaying in the booking form.

    Returns:
        Renders the booking form with doctors or error message based on validation results.
    """
    if request.method == 'POST':
        name = request.POST.get('name')
        address = request.POST.get('address')
        doctor_id = request.POST.get('doctor')
        booking_time_str = request.POST.get('booking_time')

        try:
            booking_time = datetime.strptime(booking_time_str, '%H:%M').time()
        except ValueError:
            error_message = "Invalid time format"
            return render(request, 'booking.html', {'error_message': error_message})
        
        doctor = Doctor.objects.get(id=doctor_id)
        
        # Check if the selected time is within the doctor's working hours
        if not (doctor.start_time <= booking_time <= doctor.end_time):
            error_message = "Selected time is not within doctor's working hours"
            return render(request, 'booking.html', {'error_message': error_message})
        
        # Check if the doctor is already booked at the selected time
        existing_booking = Booking.objects.filter(doctor=doctor, booking_time=booking_time).exists()
        if existing_booking:
            error_message = f"This time slot is already booked for Dr{doctor.name}. Please select another time."
            return render(request, 'booking.html', {'error_message': error_message})
        
        # Check if the doctor has available slots for booking
        available_slot = 5
        total_bookings = Booking.objects.filter(doctor=doctor).count()
        if total_bookings >= available_slot:
            error_message = f"Dr {doctor.name} has reached the maximum number of bookings. Please select another doctor."
            return render(request, 'booking.html', {'error_message': error_message})

        # If everything is fine, create the booking
        booking = Booking(name=name, address=address, doctor=doctor, booking_time=booking_time)
        booking.save()  
        return redirect('booking_success')
    
    else:
        doctors = Doctor.objects.all() 
        return render(request, 'booking.html', {'doctors': doctors})



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



# this aboutus veiws.py function
@never_cache
def aboutus(request):
    """
    View to render the about us page.

    Renders the 'aboutus.html' template.

    Args:
        request (HttpRequest): The request object.

    Returns:
        HttpResponse: Rendered HTML template for about us page.
    """
    return render(request,'aboutus.html')


# this is booking_details views.py function
@never_cache
def booking_details(request):

    """
    View function to display booking details.

    Retrieves all booking objects from the database and renders
    them on the 'bookingdetails.html' template.

    Parameters:
    - request: HttpRequest object

    Returns:
    - Rendered HttpResponse object containing the booking details
      displayed on the 'bookingdetails.html' template.
    """

    bookings = Booking.objects.all()
    return render(request,'bookingdetails.html',{'bookings':bookings})



# this is cancel_booking vews.py function
@never_cache
def cancel_booking(request,booking_id):

    """
    View function to cancel a specific booking.

    Retrieves the booking object with the given booking ID from the database,
    deletes it, and then renders the 'booking.html' template.

    Parameters:
    - request: HttpRequest object
    - booking_id: Integer representing the ID of the booking to be canceled

    Returns:
    - Rendered HttpResponse object containing the 'booking.html' template
    """
    
    booking = get_object_or_404(Booking, pk=booking_id)
    booking.delete()
    return render(request,'booking.html')


# this is IND hospitals list
def indian(request):
    mcare = Hospital.objects.all()
    return render(request,'india.html',{'mcare':mcare})

# this is UAE hospitals list
def uae(request):
    return render(request,'abudhabi.html')

# this is CANADA hospitals list
def canada(request):
    return render(request,'canada.html')