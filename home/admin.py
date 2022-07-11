from django.contrib import admin
from .models import *


# Register your models here.
admin.site.register(Subject)
admin.site.register(Student)
admin.site.register(Faculty)
admin.site.register(StudentAttendences)
admin.site.register(StudentAttendenceBlock)