from constants import *
from utils import *
from django.http import JsonResponse
from django.views.decorators.cache import never_cache
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render,redirect,get_object_or_404
from django.core.cache import cache
from .models import Doctor,Booking,Hospital,Countries,Location,Department,Banner_Cards
from accounts.models import UserProfile
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
import json
import logging

logger = logging.getLogger(__name__)

# this home views.py function
def home(request):
    """
    Home view.

    Renders the home page with the username of the logged-in user.
    
    Parameters:
    - request: The HTTP request object.
    
    Returns:
    - Renders the home page template with the username.
    """
    user = request.user 
    image = Banner_Cards.objects.all()
    return render(request, 'home.html',{'user': user,'image':image})

# this my doctors views function
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
        doctors = Doctor.objects.prefetch_related('location', 'department','location__country').all()
        cache.set('doctors_cache', doctors, timeout=60)  # Cache indefinitely since doctor details might rarely change
    return render(request, 'doctor.html', {'doctors': doctors})

# this my find_doctor views function
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
    else:
        hospital_id = request.GET.get('hospital_id')
        # locations = Location.objects.prefetch_related('name','country').all()
        selected_location = None
        if hospital_id:
            try:
                hospital = Hospital.objects.get(id=hospital_id)
                selected_location = hospital.location
            except ObjectDoesNotExist:
                error_message = "Hospital does not exist."
                return render(request, 'finddoctor.html', {'error_message': error_message})

        context = {
            'locations': Location.objects.prefetch_related('country').all(),  
            'selected_location': selected_location,
            'departments': Department.objects.all()  
        }
    
    # Render template with context  
    return render(request, 'finddoctor.html', context)



# this user booking views.py function
def booking(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            # Handle form submission
            name = request.POST.get('name')
            address = request.POST.get('address')
            doctor_id = request.POST.get('doctor')
            booking_date = request.POST.get('booking_date')
            morning_choice = request.POST.get('morning_choice')
            noon_choice = request.POST.get('noon_choice')

            selected_time = morning_choice if morning_choice else noon_choice

            doctor = Doctor.objects.get(id=doctor_id)
            
            if not (morning_choice and noon_choice):
                if morning_choice:
                    noon_choice = None
                elif noon_choice:
                    morning_choice = None

            selected_time = convert_to_time(selected_time)

            existing_booking = Booking.objects.filter(
                            doctor_id=doctor_id, booking_time=selected_time,booking_date=booking_date).exists()
            if existing_booking: 
                error_message = BOOKED_TIME_SLOT_ERROR.format(doctor_name=doctor.name)
                return JsonResponse({'success': False, 'error_message': error_message})
            
            available_slot = doctor.slot
            total_bookings = Booking.objects.filter(doctor=doctor).count()
            if total_bookings >= available_slot:
                error_message = MAX_BOOKING_REACHED_ERROR.format(doctor_name=doctor.name)
                return JsonResponse({'success': False, 'error_message': error_message})
            
            selected_time_str = convert_to_string(selected_time)

            request.session['booking_data'] = {
                'name': name,
                'address': address,
                'doctor_id': doctor_id,
                'selected_time': selected_time_str,
                'booking_date': booking_date,
            }
            return redirect('payment_page')
        else:
            # Handle initial GET request
            doctor_id = request.GET.get('doctor_id')
            doctors = Doctor.objects.prefetch_related('department', 'location', 'location__country').all()
            selected_doctor = None
            if doctor_id:
                try:
                    selected_doctor = Doctor.objects.get(id=doctor_id)
                except Doctor.DoesNotExist:
                    error_message = DOCTOR_NOT
                    return render(request, 'booking.html', {'doctors': doctors, 'error_message': error_message})

            morning_choices = generate_time_choices(9, 12)
            noon_choices = generate_time_choices(15, 20)
            return render(request, 'booking.html', {
                'doctors': doctors,
                'morning_choices': morning_choices,
                'noon_choices': noon_choices,
                'selected_doctor': selected_doctor
            })
    else:
        return redirect('login')



# this aboutus veiws.py function
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
    if request.user.is_authenticated:
        bookings = Booking.objects.filter(user=request.user)
        return render(request,'bookingdetails.html',{'bookings':bookings})
    return render(request,'login.html')



# this is cancel_booking vews.py function
def cancel_booking(request, booking_id):
    """
    View function to cancel a specific booking.

    Retrieves the booking object with the given booking ID from the database,
    deletes it, and then returns a JSON response for AJAX requests or renders
    the 'bookingdetails.html' template for non-AJAX requests.

    Parameters:
    - request: HttpRequest object
    - booking_id: Integer representing the ID of the booking to be canceled

    Returns:
    - JSON response for AJAX requests
    - Rendered HttpResponse object containing the 'bookingdetails.html' template
      for non-AJAX requests
    """
    
    booking = get_object_or_404(Booking, pk=booking_id)
    booking.delete()

    if request.is_ajax():
        return JsonResponse({'message': 'Booking canceled successfully!'})
    
    message = BOOKING_CANCELED
    return render(request, 'bookingdetails.html', {'message': message})
    

@login_required
@require_POST
def save_doctor(request, doctor_id):
    try:
        user_profile = request.user.userprofile
        doctor = get_object_or_404(Doctor, id=doctor_id)
        data = json.loads(request.body)
        action = data.get('action')
        if action == 'save':
            user_profile.saved_doctors.add(doctor)
            return JsonResponse({'success': True})
        elif action == 'unsave':
            user_profile.saved_doctors.remove(doctor)
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False})
    except Exception as e:
        logger.error(f"Error saving doctor: {e}")
        return JsonResponse({'success': False})

@login_required
def saved_doctors(request):
    user_profile = request.user.userprofile
    saved_doctors_list = user_profile.saved_doctors.all()
    return render(request, 'saved_doctors.html', {'saved_doctors': saved_doctors_list})

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
    indian_hospitals = Hospital.objects.filter(country=india).select_related('country','location')
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
    uae_hospitals = Hospital.objects.filter(country=uae).select_related('location','country')
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
    canada_hospitals = Hospital.objects.filter(country=canada).select_related('location','country')
    return render(request, 'canada_hospital_list.html', {'canada_hospitals': canada_hospitals})

# this json get view function
def get_departments_for_location(request, location_id):
    """
    Get departments associated with a location and return them as JSON.

    Args:
        request: HTTP request object.
        location_id: ID of the location.

    Returns:
        JSON response containing department IDs and names for the specified location.
    """
    location = Location.objects.get(pk=location_id)
    departments = Department.objects.filter(location=location)
    data = [{'id': department.id, 'name': department.name} for department in departments]
    return JsonResponse(data, safe=False)
