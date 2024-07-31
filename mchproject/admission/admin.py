from django.contrib import admin
from .models import Student, Course
from django.http import HttpResponse
from openpyxl import Workbook

class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'slots')
    list_filter = ['name']

class StudentsAdmin(admin.ModelAdmin):
    list_display =('first_name','last_name','date_of_birth','email','phone_number','address','course')
    list_filter = ['first_name']
    actions = ['download_admissions']

    def download_admissions(self,request,queryset):
        response = HttpResponse (content_type='application/vnd.openxmlformats-officedocument.spredsheetml.sheet')
        response['Content-Disposition'] = 'attachment;filename="admissions.xlsx"'

        wb = Workbook()
        ws = wb.active
        ws.append(['ID','FirstName','LastName','Date-of-Birth','Email','PhoneNumber','Adress','Course'])

        for admissions in queryset:
            course_info = f'{admissions.course.name}'
            ws.append([admissions.id, admissions.first_name,admissions.last_name,admissions.date_of_birth,admissions.email,admissions.phone_number,admissions.address,course_info])

        wb.save(response)
        return response

    download_admissions.short_description = "Download The Selected Admission Details"

admin.site.register(Course,CourseAdmin)
admin.site.register(Student,StudentsAdmin)
