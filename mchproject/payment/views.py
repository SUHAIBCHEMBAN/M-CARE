from datetime import datetime
from django.shortcuts import render, redirect
from details.models import Booking, Doctor
from mchproject.settings import RAZORPAY_API_KEY, RAZORPAY_API_SECRET_KEY
import razorpay
from constants import *


def doctor_payment(request):
    """
    View function to handle doctor payment processing.

    This function retrieves booking data from the session, processes the payment using Razorpay API,
    and renders the payment page with necessary context.

    Args:
        request: Django HTTP request object.

    Returns:
        HTTP response rendering the payment page or an error page if any exception occurs.
    """

    # Retrieve booking data from session
    booking_data = request.session.get('booking_data')
    if not booking_data:
        return redirect('booking')

    try:
        # Extract necessary booking details
        booking_time = datetime.strptime(booking_data['booking_time'], '%H:%M').time()
        doctor_id = booking_data['doctor_id']
        doctor = Doctor.objects.get(id=doctor_id)
        doctor_name = doctor.name
        doctor_charge = doctor.charge
        department = doctor.department

        user_name = booking_data.get('name')
        user_address = booking_data.get('address')
    except (ValueError, Doctor.DoesNotExist) as e:
        # Handle exceptions related to booking data retrieval
        error_message = BOOKING_PROCESS
        return render(request, 'error.html', {'error_message': error_message})

    try:
        # Initialize Razorpay client and create payment order
        client = razorpay.Client(auth=(RAZORPAY_API_KEY, RAZORPAY_API_SECRET_KEY))
        amount = doctor_charge * 100  # Convert charge to paisa (Razorpay expects amount in smallest currency unit)
        payment_order = client.order.create(data={
            "amount": amount,
            "currency": "INR",
            "receipt": "receipt#1",
            "notes": {
                "key1": "value3",
                "key2": "value2"
            }
        })
        payment_order_id = payment_order['id']
    except Exception as e:
        # Handle exceptions related to payment processing
        error_message = PAYMENT_PROCESS
        return render(request, 'error.html', {'error_message': error_message})

    # Prepare context for rendering payment page
    context = {
        'api_key': RAZORPAY_API_KEY,
        'order_id': payment_order_id,
        'doctor_name': doctor_name,
        'doctor_charge': doctor_charge,
        'user_name': user_name,
        'user_address': user_address,
        'booking_time': booking_time,
        'department':department,
    }
    return render(request, 'payment.html', context)


def booking_success(request):
    """
    View function to handle booking success.

    This function creates a booking entry in the database, deletes booking data from the session,
    and renders the booking success page.

    Args:
        request: Django HTTP request object.

    Returns:
        HTTP response rendering the booking success page or redirecting to the booking page if no booking data found.
    """
    # Retrieve booking data from session
    booking_data = request.session.get('booking_data')
    if not booking_data:
        return redirect('booking')

    # Create booking entry in the database
    booking_time = datetime.strptime(booking_data['booking_time'], '%H:%M').time()
    doctor = Doctor.objects.get(id=booking_data['doctor_id'])
    booking = Booking.objects.create(
        name=booking_data['name'],
        address=booking_data['address'],
        doctor=doctor,
        booking_time=booking_time,
        user=request.user
    )

    # Remove booking data from session
    del request.session['booking_data']

    return render(request, 'booking_success.html', {'booking': booking})