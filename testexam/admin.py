from django.contrib import admin

# Register your models here.
from testexam.models import Exam, Questions, Subject, faculty, Student

admin.site.register(Student)
admin.site.register(Exam)
admin.site.register(Questions)
admin.site.register(Subject)
admin.site.register(faculty)
