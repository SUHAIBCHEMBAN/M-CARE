from django.shortcuts import render
from .forms import StudentForm
from .models import Course, Student
from django.core.mail import send_mail
from django.core.exceptions import ValidationError
from django.http import JsonResponse

def student_admission(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            try:
                student = form.save()
                mail_subject = 'M-CARE HOSPITAL'
                message = 'Your Admission Approved'
                recipient_list = [student.email]
                send_mail(mail_subject, message, 'your_email@example.com', recipient_list)
                return JsonResponse({'success': True, 'message': 'Your admission is approved!'})
            except ValidationError as e:
                return JsonResponse({'success': False, 'error': e.message}, status=400)
        else:
            return JsonResponse({'success': False, 'errors': form.errors}, status=400)
    else:
        courses = Course.objects.all()
        course_slots = [(course, course.slots - course.student_set.count()) for course in courses]
        return render(request, 'admissionform.html', {'courses': course_slots})
