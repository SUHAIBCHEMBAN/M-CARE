from django.shortcuts import render,redirect,get_object_or_404
# from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from datetime import datetime
from django.core.cache import cache
from .models import Doctor,Booking,Hospital,Countries,Location,Department
from constants import (
    INVALID_TIME_FORMAT_ERROR,
    DOCTOR_WORKING_HOURS_ERROR,
    BOOKED_TIME_SLOT_ERROR,
    MAX_BOOKING_REACHED_ERROR,
    LOGIN_REQUIRED_ERROR,
    NO_DOCTOR_FOUND_MESSAGE
)
# Create your views here.

# this home views.py function
@never_cache  
def home(request):
    """
    Home view.

    Renders the home page with the username of the logged-in user.
    
    Parameters:
    - request: The HTTP request object.
    
    Returns:
    - Renders the home page template with the username.
    """
    return render(request, 'home.html',)

@never_cache
def doctors(request):
    """
    View function for displaying a list of doctors.

    Retrieves all doctors from the database.
    Renders the 'doctor.html' template with the list of doctors.
    
    :param request: The HTTP request object.
    :return: The rendered HTML page displaying the list of doctors.
    """
    doctors = cache.get('doctors_cache')  # Check if doctors data is cached
    if not doctors:
        # If data is not cached, retrieve from database and cache it
        doctors = Doctor.objects.all()
        cache.set('doctors_cache',doctors,timeout=120) # Cache for 2 minutes (120 seconds)
    return render(request, 'doctor.html', {'doctors': doctors})


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
        location_id = request.POST.get('location')
        department_id = request.POST.get('department')
        
        # Retrieve location and department names
        location = Location.objects.get(id=location_id)
        department = Department.objects.get(id=department_id)
        
        # Generate cache key based on location and department
        cache_key = f"doctors_{location.name}_{department.name}"
        
        # Check if data is cached
        doctors = cache.get(cache_key)
        
        # If data is not cached, retrieve it from the database
        if not doctors:
            doctors = Doctor.objects.filter(location=location, department=department)
            
            # Cache the data for 2 minutes
            cache.set(cache_key, doctors, timeout=120)
        
        # If no doctors found, render template with message
        if not doctors:
            message = NO_DOCTOR_FOUND_MESSAGE
            return render(request, 'filtered_doctors.html', {'message': message})
        
        # Render template with list of doctors
        return render(request, 'filtered_doctors.html', {'doctors': doctors})
    
    # If request method is not POST, populate context with locations and departments
    context = {
        'locations': Location.objects.all(),  
        'departments': Department.objects.all()  
    }
    
    # Render template with context
    return render(request, 'finddoctor.html', context)
    

# this user booking views.py function
# @login_required
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
    if request.user.is_authenticated:
        if request.method == 'POST':
            name = request.POST.get('name')
            address = request.POST.get('address')
            doctor_id = request.POST.get('doctor')
            booking_time_str = request.POST.get('booking_time')

            try:
                booking_time = datetime.strptime(booking_time_str, '%H:%M').time()
            except ValueError:
                error_message = INVALID_TIME_FORMAT_ERROR
                return render(request, 'booking.html', {'error_message': error_message})
        
            doctor = Doctor.objects.get(id=doctor_id)
        
            # Check if the selected time is within the doctor's working hours
            if not (doctor.start_time <= booking_time <= doctor.end_time):
                error_message = DOCTOR_WORKING_HOURS_ERROR.format(start_time=doctor.start_time, end_time=doctor.end_time)
                return render(request, 'booking.html', {'error_message': error_message})
        
            # Check if the doctor is already booked at the selected time
            existing_booking = Booking.objects.filter(doctor=doctor, booking_time=booking_time).exists()
            if existing_booking: 
                error_message = BOOKED_TIME_SLOT_ERROR.format(doctor_name=doctor.name)
                return render(request, 'booking.html', {'error_message': error_message})
        
            # Check if the doctor has available slots for booking
            available_slot = 5
            total_bookings = Booking.objects.filter(doctor=doctor).count()
            if total_bookings >= available_slot:
                error_message = MAX_BOOKING_REACHED_ERROR.format(doctor_name=doctor.name)
                return render(request, 'booking.html', {'error_message': error_message})

            # If everything is fine, create the booking
            booking = Booking(name=name, address=address, doctor=doctor, booking_time=booking_time)
            booking.save()  
            return redirect('booking_success')
    
        else:
            doctors = Doctor.objects.all() 
            return render(request, 'booking.html', {'doctors': doctors})
    else:
        # messages.info(request, 'You need to be logged in to access the booking page.')
        error_message = LOGIN_REQUIRED_ERROR
        return redirect('login')



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
    """
    View function to display a list of Indian hospitals.

    Retrieves all hospitals in India from the database and passes them to the template for rendering.

    Parameters:
        request (HttpRequest): The request object sent by the client.

    Returns:
        HttpResponse: The HTTP response containing the rendered template with the list of Indian hospitals.
    """
    india = Countries.objects.get(name='India')
    indian_hospitals = Hospital.objects.filter(country=india)
    return render(request, 'indian_hospital_list.html', {'indian_hospitals': indian_hospitals})


# this is UAE hospitals list
def uae(request):
    """
    View function to display a list of hospitals in the UAE (United Arab Emirates).

    Retrieves all hospitals in the UAE from the database and passes them to the template for rendering.

    Parameters:
        request (HttpRequest): The request object sent by the client.

    Returns:
        HttpResponse: The HTTP response containing the rendered template with the list of UAE hospitals.
    """
    uae = Countries.objects.get(name='UAE')
    uae_hospitals = Hospital.objects.filter(country=uae)
    return render(request, 'abudhabi_hospital_list.html', {'uae_hospitals': uae_hospitals})


# this is CANADA hospitals list
def canada(request):
    """
    View function to display a list of hospitals in Canada.

    Retrieves all hospitals in Canada from the database and passes them to the template for rendering.

    Parameters:
        request (HttpRequest): The request object sent by the client.

    Returns:
        HttpResponse: The HTTP response containing the rendered template with the list of Canadian hospitals.
    """
    canada = Countries.objects.get(name='Canada')
    canada_hospitals = Hospital.objects.filter(country=canada)
    return render(request, 'canada_hospital_list.html', {'canada_hospitals': canada_hospitals})


from django.http import JsonResponse

def get_departments_for_location(request, location_id):
    location = Location.objects.get(pk=location_id)
    departments = Department.objects.filter(location=location)
    data = [{'id': department.id, 'name': department.name} for department in departments]
    return JsonResponse(data, safe=False)
