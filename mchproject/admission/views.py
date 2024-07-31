from django.shortcuts import render, redirect
from .forms import StudentForm
from .models import Course
from django.core.exceptions import ValidationError

def student_admission(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                return redirect('student_admission_success')
            except ValidationError as e:
                return render(request, 'admissionform.html', {'error_message': e.message, 'form_data': request.POST})
    else:
        courses = Course.objects.all()
        course_slots = []
        for course in courses:
            available_slots = course.slots - course.student_set.count()
            course_slots.append((course, available_slots))

    return render(request, 'admissionform.html', {'courses': course_slots})

def student_admission_success(request):
    return render(request, 'admissionsuccess.html')
