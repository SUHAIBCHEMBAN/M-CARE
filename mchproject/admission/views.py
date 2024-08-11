from django.shortcuts import render
from .forms import StudentForm
from .models import Course, Student
from django.core.mail import send_mail
from django.core.exceptions import ValidationError
from django.http import JsonResponse

def student_admission(request):
    """
    Handles the student admission process. 
    If the request method is POST, it processes the submitted admission form, saves the student details,
    assigns the currently logged-in user to the student, and sends a confirmation email. 
    If the request method is GET, it renders the admission form with available courses and their remaining slots.

    Parameters:
    request (HttpRequest): The request object containing metadata about the request.

    Returns:
    JsonResponse: A JSON response indicating the success or failure of the admission submission.
    If GET request, renders the 'admissionform.html' template with course data.
    """
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            try:
                student = form.save(commit=False)  # Create the student instance without saving to DB
                student.user = request.user        # Assign the logged-in user to the student
                student.save()                     # Now save the student object to the database
                
                # Send confirmation email
                mail_subject = 'M-CARE HOSPITAL'
                message = 'Your Admission Approved'
                recipient_list = [student.email]
                send_mail(mail_subject, message, 'your_email@example.com', recipient_list)
                
                return JsonResponse({'success': True, 'message': "Your admission has been approved! Our team will contact you shortly."})
            except Exception as e:  # Use a general exception if needed
                return JsonResponse({'success': False, 'error': str(e)}, status=400)
        else:
            return JsonResponse({'success': False, 'errors': form.errors}, status=400)
    else:
        courses = Course.objects.all()
        course_slots = [(course, course.slots - course.student_set.count()) for course in courses]
        return render(request, 'admissionform.html', {'courses': course_slots})

def admission_details(request):
    """
    Displays the admission details for the currently logged-in user.
    If the user is authenticated, it retrieves the student's admission details associated with the user.
    If the user is not authenticated, it redirects them to the login page.

    Parameters:
    request (HttpRequest): The request object containing metadata about the request.

    Returns:
    HttpResponse: Renders the 'admissiondetails.html' template with the student's admission data.
    If the user is not authenticated, renders the 'login.html' template.
    """
    if request.user.is_authenticated:
        admissions = Student.objects.filter(user=request.user)
        return render(request, 'admissiondetails.html', {'admissions': admissions})
    return render(request, 'login.html')
