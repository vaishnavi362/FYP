from __future__ import division
from django.db import models
from datetime import datetime 
from django.contrib.auth.models import User
from django.urls import reverse
from datetime import datetime
from jsonfield import JSONField



"""
pip install pillow
pip install pandas
pip install twilio
pip install jsonfield

"""
GENDER_CHOUCE   = (('MALE','MALE'), ('FEMALE','FEMALE'))
SUBJECT_CHOUCE  = (('M1', 'M1'), ('M2', 'M2'), ('BEEE', 'BEEE'), ('ENGLISH', 'ENGLISH'), ('SCIENCE', 'SCIENCE'))
BRANCH_CHOUCE   = (('E & C','E & C'), ('MECHANICAL','MECHANICAL'), ('COMPUTER SCIENCE','COMPUTER SCIENCE'))
SEM_CHOUCE      = ((1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8),)
DIVISION_CHOUCE = (('A', 'A'), ('B', 'B'), ('C', 'C'))
PHONE           = (('8197424203', '8197424203'), ('8747972557', '8747972557'), ('9663172677', '9663172677'), ('9986168736', '9986168736'))

class Faculty(models.Model):
    fid             = models.AutoField(primary_key=True)
    user_id         = models.CharField(max_length = 30, default='')
    first_name      = models.CharField(max_length = 30, default='')
    last_name       = models.CharField(max_length = 30, default='')
    image           = models.ImageField(upload_to='faculties/', null = True, blank = True)
    date_of_birth   = models.DateField(default=datetime.now(), blank = True)
    date_of_joining = models.DateField(default=datetime.now(), blank = True)
    email           = models.EmailField(max_length = 30, default = 'email',)
    gender          = models.CharField(max_length = 30, default = 'MALE', choices = GENDER_CHOUCE)
    degree          = models.CharField(max_length = 30, default = '')
    branch          = models.CharField(max_length = 30,  choices = BRANCH_CHOUCE)
    created_date    = models.DateField(auto_now_add = True)
    status          = models.BooleanField(default = 0)
    phone           = models.CharField( max_length = 30, default = '')

    def __str__(self):
        return self.first_name + ' ' + self.last_name

    def get_absolute_url(self):
        return reverse("faculties")
        # return reverse("faculties", args = (str(self.id)))
    def class_name(self):
        return 'faculty'


class Student(models.Model):
    usn             = models.AutoField(primary_key=True)
    user_id         = models.CharField(max_length = 30, default='')
    student_usn     = models.CharField(max_length = 30, unique = True)
    first_name      = models.CharField(max_length = 30, default='')
    last_name       = models.CharField(max_length = 30, default='')
    image           = models.ImageField(upload_to='students/', null = True, blank = True)
    date_of_birth   = models.DateField(default=datetime.now(), blank=True)
    date_of_joining = models.DateField(default=datetime.now(), blank=True)
    email           = models.EmailField(max_length = 30, default='email',)
    gender          = models.CharField(max_length = 10, default = 'MALE', choices = GENDER_CHOUCE)
    branch          = models.CharField(max_length = 30, choices = BRANCH_CHOUCE)
    division        = models.CharField(max_length = 30, choices = DIVISION_CHOUCE)
    sem             = models.IntegerField(choices = SEM_CHOUCE)
    created_date    = models.DateField(auto_now_add = True)
    status          = models.BooleanField(default = 0)
    phone           = models.CharField(max_length = 30, default = '')

    def __str__(self):
        return self.first_name + ' ' + self.last_name

    def get_absolute_url(self):
        return reverse("students1")

    def class_name(self):
        return 'student'

class Subject(models.Model):
    id       = models.AutoField(primary_key=True)
    sub_name = models.CharField(max_length = 30, default='add first name')
    sem      = models.IntegerField( choices = SEM_CHOUCE)

class StudentAttendences(models.Model):
    id              = models.AutoField(primary_key=True)
    student_usn     = models.CharField(max_length = 30)
    status          = models.BooleanField()
    branch          = models.CharField(max_length = 30, choices = BRANCH_CHOUCE)
    division        = models.CharField(max_length = 30, choices = DIVISION_CHOUCE)
    subject         = models.CharField(max_length = 30, choices = SUBJECT_CHOUCE)
    sem             = models.IntegerField(choices = SEM_CHOUCE)
    date            = models.DateField()
    previous_hash   = models.CharField(max_length = 255, default='')
    attendenceBlock = JSONField(null=False, default= {})
    

    def __str__(self):
        return self.student_usn + ' ' + str(self.date) + ' ' + str(self.sem) + ' ' + self.branch

class StudentAttendenceBlock(models.Model):
    branch          = models.CharField(max_length = 30, choices = BRANCH_CHOUCE)
    division        = models.CharField(max_length = 30, choices = DIVISION_CHOUCE)
    subject         = models.CharField(max_length = 30, choices = SUBJECT_CHOUCE)
    sem             = models.IntegerField(choices = SEM_CHOUCE)
    previous_hash   = models.CharField(max_length = 255, default='')
    attendenceBlock = JSONField(null=False, default= {})
    date            = models.DateField()
    
