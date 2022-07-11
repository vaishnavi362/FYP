from dataclasses import field
from pickle import TRUE
from tempfile import tempdir
from webbrowser import get
from django.shortcuts import render, redirect
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth import authenticate, login, logout
# from django.contrib.auth.decorators import login_required
from .models import *
from django.urls import reverse_lazy
from django.contrib import messages #import messages
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.core.mail import send_mail
from home.blockchain import Blockchain as _blockchain
import csv
from django.http import HttpResponse
import pandas as pd
from twilio.rest import Client
import random as r


BRANCH_CHOUCE   = (('E & C','E & C'), ('MECHANICAL','MECHANICAL'), ('COMPUTER SCIENCE','COMPUTER SCIENCE'))
ACCOUNT_SID = "ACff469b87e19877056d4b9514ca71a508"
AUTH_TOKEN  = "72d2a6e3115a67ea042354db1ba6c2a5"
FROM        = "+19895751647"
TO          = "+91"

# account_sid = "ACff469b87e19877056d4b9514ca71a508"
# auth_token  = "a1178b5405d1d781b2463cacfd1d2b73"
# client = Client(account_sid, auth_token)
# message = client.messages.create(
#                 body="Hiii",
#                 to="+919989168736",
#                 from_="+19895751647",
#                 )

# print(message.sid)
previos_hash1 = StudentAttendenceBlock.objects.all()
if not previos_hash1:
    previos_hash1 = 10
else:
    previos_hash1 = StudentAttendenceBlock.objects.all()[::-1][0].previous_hash
print('previos_hash ===>', previos_hash1)
Blockchain = _blockchain(prev= previos_hash1)


def generate_random_password():
    password = r.randint(1111111, 2222222)
    return password

class ForgotPassword(TemplateView):
    template_name = 'forgot_password.html'
    def post(self, request):
        #faculty forgot password
        user_id = self.request.POST['phone']
        if user_id :# if valid phone number
            if 'faculty' in self.request.POST :
                faculty = Faculty.objects.filter(user_id = user_id).first()
                if faculty:  
                    user = User.objects.filter(last_name = faculty.pk, first_name = 'faculty').first()
                    if user:
                        usr = User.objects.get(username = user.username)
                        print(user.username,'----------')
                        reset_password = str(generate_random_password())
                        print(reset_password,'|||\\\\\\\\')
                        usr.set_password(reset_password)
                        usr.save()
                        context = {'success' : f'Faculty password reset successfully. your username is {user.username} and password is {reset_password}.'}
                    else:
                        context = {'error' : 'User is not added please contact admin'}
                else :
                    context = {'error': 'Please enter valid phone number, provided number is not linked with any faculty'}
            else :
                student = Student.objects.filter(user_id= user_id).first()
                if student:  
                    user = User.objects.filter(last_name = student.pk, first_name = 'student').first()
                    if user:
                        usr = User.objects.get(username = user.username)
                        print(user.username,'----------')
                        reset_password = str(generate_random_password())
                        usr.set_password(reset_password)
                        usr.save()
                        context = {'success' : f'Student password reset successfully. your username is {user.username} and password is {reset_password}.'}
                    else:
                        context = {'error' : 'User is not added please contact admin'}
                else :
                    context = {'error': 'Please enter valid phone number, provided number is not linked with any student'}
        else : 
            context = {'error': 'Please enter valid phone number'}
        return render(request, self.template_name, context)

def _send_message(message):
    client  = Client(ACCOUNT_SID, AUTH_TOKEN)
    message = client.messages.create(
                body  = message,
                to    = TO,
                from_ = FROM,
    )
    return

def send_message(request, pk):
    student_id = pk
    student = Student.objects.filter(usn = student_id).first()
    student_usn = student.student_usn
    student_name = f"{student.first_name} {student.last_name}"
    student_all_att = StudentAttendences.objects.filter(student_usn = student_usn)
    student_attendence = dict()
    final_attendence   = dict()
    # initilize all subjects with 0 calaulation
    for subject, s in SUBJECT_CHOUCE:
        student_attendence[subject] = {'present' : 0, 'absent' : 0,'total' : 0}
        final_attendence[subject] = {'percentage' : 0}
    # calculate attendence
    for attendence in student_all_att:
        # if attendence.status:
        if attendence.attendenceBlock['data'][student_usn]:# fetching data from blockchain
            student_attendence[attendence.subject]['present'] += (1 + 0)
        else:
            student_attendence[attendence.subject]['absent'] += (1 + 0)
        student_attendence[attendence.subject]['total'] += 1

    # df = pd.DataFrame(student_attendence)
    # print(df)       
    for sub, att in student_attendence.items():
        if att['total'] == 0:
            final_attendence[sub]['percentage'] = 'no atendence'
            # final_attendence[sub]['color']      = 'red'
        else:
            floa = (att['present'] / att['total']) * 100
            format_float = "{:.2f}".format(floa)
            final_attendence[sub]['percentage'] = format_float
            # if floa >= 75:
            #     final_attendence[sub]['color']  = 'green'
            # else:
            #     final_attendence[sub]['color']  = 'red'

    message = f'student USN = {student_usn}; Student name : {student_name}; '
    for sub, attendence  in final_attendence.items():
        message = f"{message} {sub} : {attendence['percentage']}%; "
    _send_message(message)

    return redirect('students1')


class HomPage(TemplateView):
    template_name = "home1.html"
    # template_name = "home.html"
    def get(self, request):
        if request.user.is_authenticated:
            if request.user.is_superuser: # if superuser then redirect to faculty page
                return redirect('faculties')
            elif request.user.is_staff: # if is faculty redirect  to studets page
                return redirect('students1')
            elif not request.user.is_staff and not request.user.is_superuser:
                return redirect ('student_details', pk = request.user.last_name)
        else:
            # return redirect('home')
            return render(request, template_name = self.template_name)

class RegisterStudentPage(CreateView):
    template_name = "register.html"
    model         = Student
    fields        = ['student_usn', 'first_name', 'last_name', 'date_of_birth', 'date_of_joining', 'email', 'gender', 'branch', 'division', 'sem', 'image', 'phone']
        
    # def get_queryset(self):
    #     return super().get_queryset()
    def get_context_data(self, **kwargs):
        context               = super().get_context_data(**kwargs)
        context["header"]     = 'Register'
        context["button"]     = 'Register'
        context["background"] = '/static/home/images/register_stugent1.jpg'
        return context
    

class UpdateStudent(UpdateView):
    template_name = "register.html"
    model         = Student
    fields        = ['student_usn', 'first_name', 'last_name', 'date_of_birth', 'date_of_joining', 'email', 'gender', 'branch', 'division', 'sem', 'image', 'phone']

    def get_context_data(self, **kwargs):
        context               = super().get_context_data(**kwargs)
        context["header"]     = "Update"
        context["button"]     = "Update"
        context["background"] = '/static/home/images/register_stugent1.jpg'
        return context
    

class DeleteStudent(DeleteView):
    template_name = "register.html"
    model         = Student
    success_url   = reverse_lazy('students1')

    def get_context_data(self, **kwargs):
        context               = super().get_context_data(**kwargs)
        context["header"]     = 'Are you sure you want to delete!'
        context["button"]     = 'Delete'
        context["background"] = '/static/home/images/register_stugent1.jpg'
        return context



class FacultiesPage(ListView):
    model         = Faculty
    template_name = "faculties.html"

class StudentList(ListView):
    model         = Student
    template_name = "students.html"
    
  



class StudentLis1t1(ListView):
    model         = Student
    template_name = "students1.html"
    
    def get_queryset(self, **kwargs):
       qs = super().get_queryset(**kwargs)
       faculty_id         = self.request.user.last_name
       faculty_branch     = Faculty.objects.get(pk = faculty_id).branch
       return qs.filter(branch = faculty_branch)    

class StudentAttendenceCredentials(TemplateView):
    template_name = "select_attendence_credentials.html"

    def post(self, request, *args, **kwargs):
        request.session['subject']  = request.POST['subject']
        request.session['sem']      = request.POST['sem']
        request.session['branch']   = request.POST['branch']
        request.session['division'] = request.POST['division']
        request.session['sdate']    = request.POST['sdate']
        return redirect('student_attendenct')

class StudentAttendence(ListView):
    model         = Student
    template_name = "student_attendence.html"
    success_url = reverse_lazy('faculties')

def student_attendence(request):
    if request.method == 'GET':
        validate = StudentAttendences.objects.filter (subject = request.session['subject'], sem = request.session['sem'], branch =request.session['branch'], date = request.session['sdate'], division = request.session['division'])
        context = {
            'students' : Student.objects.filter(branch = request.session['branch'], division = request.session['division'], sem = request.session['sem']),
            'subject'  : request.session['subject'],
            'sem'      : request.session['sem'],
            'branch'   : request.session['branch'],
            'division' : request.session['division'],
            'sdate'    : request.session['sdate'],
            'config_error' : validate,
        }
        return render(request, 'student_attendence.html', context)
    else:
        students   = Student.objects.filter(branch = request.session['branch'], division = request.session['division'], sem = request.session['sem'])
        # attendence = StudentAttendences.objects.create()
        '''for stu in students:
            attendence = StudentAttendences.objects.create(branch = request.session['branch'], division = request.session['division'], sem = request.session['sem'], status = stu.student_usn in request.POST, student_usn = stu.student_usn, subject = request.session['subject'], date = request.session['sdate'])'''
        dict1 ={}
        for stu in students:
            if not Blockchain.is_chain_valid():
                print('Block is not valid')
            else :
                block = Blockchain.mine_block(data= {stu.student_usn : stu.student_usn in request.POST} )
                print('block ===>',block)
                print("block is valid")
                attendence = StudentAttendences.objects.create(branch = request.session['branch'], division = request.session['division'], sem = request.session['sem'], status = stu.student_usn in request.POST, student_usn = stu.student_usn, subject = request.session['subject'], date = request.session['sdate'], previous_hash = block["previous_hash"], attendenceBlock = block)
                dict1[stu.student_usn]=stu.student_usn in request.POST
        
        print(dict1)
        if not Blockchain.is_chain_valid():
                print('Block is not valid')
        else :
            block = Blockchain.mine_block(data= dict1)
            print('block ===>',block)
            print("block is valid")
            attendence =StudentAttendenceBlock.objects.create(branch = request.session['branch'], division = request.session['division'], sem = request.session['sem'], previous_hash = block["previous_hash"], attendenceBlock = block, subject = request.session['subject'], date = request.session['sdate'])

        ## Blockchain
        ''' if not Blockchain.is_chain_valid():
            print('Block is not valid')
        else :
            block = Blockchain.mine_block(data= str(request.POST) )
            print('block ===>',block)
            print("Block is valid") '''

        return redirect('attendence_overview') 
        # return redirect('students1') 

# SUBJECTS = {'M1' : 'M1', 'M2' : 'M2', 'ENGLISH' : 'ENGLISH', 'BEEE' : 'BEEE', 'SCIENCE' : 'SCIENCE'}

class StudentDetails(DetailView):
    model         = Student
    template_name = "student_details.html"

    def get_context_data(self, **kwargs):
        student_id = self.kwargs['pk']
        student_usn = Student.objects.filter(usn = student_id).first().student_usn
        student_all_att = StudentAttendences.objects.filter(student_usn = student_usn)
        student_attendence = dict()
        final_attendence   = dict()
        # initilize all subjects with 0 calaulation
        for subject, s in SUBJECT_CHOUCE:
            student_attendence[subject] = {'present' : 0, 'absent' : 0,'total' : 0}
            final_attendence[subject] = {'percentage' : 0}
        # calculate attendence
        for attendence in student_all_att:
            # if attendence.status:
            if attendence.attendenceBlock['data'][student_usn]:# fetching data from blockchain
                student_attendence[attendence.subject]['present'] += (1 + 0)
            else:
                student_attendence[attendence.subject]['absent'] += (1 + 0)
            student_attendence[attendence.subject]['total'] += 1

        # df = pd.DataFrame(student_attendence)
        # print(df)       
        for sub, att in student_attendence.items():
            if att['total'] == 0:
                final_attendence[sub]['percentage'] = 'no attendance'
                final_attendence[sub]['color']      = 'red'
            else:
                floa = (att['present'] / att['total']) * 100
                format_float = "{:.2f}".format(floa)
                final_attendence[sub]['percentage'] = format_float
                if floa >= 75:
                    final_attendence[sub]['color']  = 'green'
                else:
                    final_attendence[sub]['color']  = 'red'
        context                   = super().get_context_data(**kwargs)
        context['attendence']     = final_attendence
        # df = pd.DataFrame(final_attendence)
        # print(df)

        return context

def download_student_details(request, pk) :
    student_usn = Student.objects.filter(usn = pk).first().student_usn
    student_all_att = StudentAttendences.objects.filter(student_usn = student_usn)
    student_attendence = dict()
    # initilize all subjects with 0 calaulation
    for stu in student_all_att:
        if (stu.status):
            student_attendence[str(stu.date)] = {stu.subject : 'Present'}
        else:
            student_attendence[str(stu.date)] = {stu.subject : 'Absent'}
    df = pd.DataFrame(student_attendence)
    df.fillna('No atendence', inplace=True)

    print(df)  
    print('======')
    # response = HttpResponse(content_type = 'test/csv')  
    # response['content-Disposition'] = f'attachment; filename={student_usn}.csv'
    # writter = csv.writer(response, csv.excel)
    # writter.writerows(student_attendence)
    # return response
    geeks_object = df.to_html()
  
    return HttpResponse(geeks_object)
    # return redirect('student_details', pk = pk)

class FacultytDetails(DetailView):
    model         = Faculty
    template_name = "faculty_details.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        fac_id  =  self.kwargs['pk']
        if (User.objects.filter(last_name = fac_id).first()):
           context["user_id"] = User.objects.filter(last_name = fac_id).first().username
        else:
           context["user_id"] = 'User not created'
        return context

class RegisterPage(CreateView):
    template_name = "register.html"
    model         = Faculty
    fields        = ['first_name', 'last_name', 'date_of_birth', 'date_of_joining', 'email', 'gender', 'branch', 'image', 'degree', 'phone',]
        
    # def get_queryset(self):
    #     return super().get_queryset()
    def get_context_data(self, **kwargs):
        context               = super().get_context_data(**kwargs)
        context["header"]     = 'Register'
        context["button"]     = 'Register'
        context["background"] = '/static/home/images/regidter.jpg'
        return context
    

class UpdateFaculty(UpdateView):
    template_name = "register.html"
    model         = Faculty
    fields        = ['first_name', 'last_name', 'date_of_birth', 'date_of_joining', 'email', 'gender', 'branch', 'image', 'degree', 'phone',]

    def get_context_data(self, **kwargs):
        context               = super().get_context_data(**kwargs)
        context["header"]     = "Update"
        context["button"]     = "Update"
        context["background"] = '/static/home/images/regidter.jpg'
        return context
    

class DeleteFaculty(DeleteView):
    template_name = "register.html"
    model        = Faculty
    success_url  = reverse_lazy('faculties')

    def get_context_data(self, **kwargs):
        context               = super().get_context_data(**kwargs)
        context["header"]     = 'Are you sure you want to delete!'
        context["button"]     = 'Delete'
        context["background"] = '/static/home/images/regidter.jpg'
        return context

def login_page(request):
    if request.user.is_authenticated:
        if request.user.is_superuser: # if superuser then redirect to faculty page
            return redirect('faculties')
        elif request.user.is_staff: # if is faculty redirect  to studets page
            return redirect('students1')
        elif not request.user.is_staff and not request.user.is_superuser:
            return redirect ('student_details', pk = request.user.last_name)
    else:
        if (request.path == '/login_admin/'):
            path = 'register1.jpg'
            form = 'Admin'
            forg = False
        elif (request.path == '/login_faculty/'):
            path = 'home_background.jpg'
            form = 'Faculty'
            forg = True
        elif (request.path == '/login_student/'):
            path = 'students.jpg'
            form = 'Student'
            forg = True
        context = {'image' : path, 'form' : form, 'forg' : forg}
        if request.method == 'GET':
            template_name = "login.html"
        elif (request.method == 'POST'):
            if (request.path == '/login_admin/'):
                first_name = ''
                next       = '/faculties/'
            elif (request.path == '/login_faculty/'):
                first_name = 'faculty'
                next       = '/students1/'
            elif (request.path == '/login_student/'):
                first_name = 'student'
            user = authenticate(username = request.POST['username'], password = request.POST['password'], first_name = first_name)
            if user is not None :
                login(request, user)
                if  (request.path == '/login_admin/' and user.first_name != ''):
                    print('-------')
                    logout(request) # if not admin logout
                    return redirect('home')
                elif (request.path == '/login_faculty/' and user.first_name != 'faculty'):
                    logout(request) # if not admin logout
                    return redirect('home')
                if  (request.path == '/login_student/'): # if not student logout
                    next = ''
                    if (not user.is_staff and not user.is_superuser):
                        next = '/student_details/'+user.last_name
                    else :
                        logout(request)
                        return redirect('home')
                return redirect(next)
            else :
                template_name = "login.html"
                context['error'] = 'Please enter valid username and password'
        return render(request, template_name, context)

def create_user(request, pk):
    if request.user.is_authenticated:
        if request.method == 'GET':
            if (request.path == f'/create_faculty_user/{pk}'):
                path = 'create_user.jpg'
                context = {'image' : path, 'obj' : Faculty.objects.get(pk = pk, status = 0)}
            elif (request.path == f'/create_student_user/{pk}'):
                path = 'create_user.jpg'
                context = {'image' : path, 'obj' : Student.objects.get(pk = pk, status = 0)}
            template_name = 'create_user.html'
            return render(request, template_name, context)
        else:
            username = request.POST['username']
            if not  User.objects.filter(username=username).exists():
                if (request.path == f'/create_faculty_user/{pk}'):
                    faculty    = Faculty.objects.get(pk = pk)
                    email      = faculty.email
                    first_name = 'faculty'
                    is_staff   = True
                    redirect_l = "/faculties/"
                elif (request.path == f'/create_student_user/{pk}'):
                    faculty    = Student.objects.get(pk = pk)
                    email      = faculty.email
                    first_name = 'student'
                    is_staff   = False
                    redirect_l = "students1"
                password = request.POST['pwd']
                if faculty and username and password:
                    user = User.objects.create_user(first_name = first_name, last_name = pk, username = username, password = password, email = email, is_staff = is_staff)
                    user.save()
                    # faculty = Faculty.objects.get(pk = pk)
                    faculty.status = True
                    faculty.user_id = username
                    faculty.save()
                    messages.success(request, 'User created successfully')
                elif not username:
                    messages.success(request, 'Please enter username')
                elif not password:
                    messages.success(request, 'Please enter password')
                elif not faculty:
                    messages.success(request, 'Please select faculty')
                messages.success(request, 'Profile details updated.')
                return redirect(redirect_l)
            else:
                # if user exist then redirect to respective page
                if (request.path == f'/create_faculty_user/{pk}'):
                    request.session['user_error'] = 'Username already exists'
                    return redirect(f'/create_faculty_user/{pk}')
                elif (request.path == f'/create_student_user/{pk}'):
                    request.session['user_error'] = 'Username already exists'
                    return redirect(f'/create_student_user/{pk}')
    else:
            return redirect("home")

def lgout(request):
    logout(request)
    return redirect('home')

        
def attendence_overview(request):

    template_name = 'attendence_overview.html'
    if request.method == 'POST':
        subject          = request.POST['subject']
        sem              = request.POST['sem']
        branch           = request.POST['branch']
        division         = request.POST['division']
        date             = request.POST['date']

        attendence       = StudentAttendenceBlock.objects.filter(subject=subject, sem=sem, branch=branch, division=division, date=date).first()
        final_attendence = []
        if attendence:
            attendence       = attendence.attendenceBlock['data']
            for usn, status in attendence.items():
                student = Student.objects.filter(student_usn = usn).first()
                image = student.image
                name  = f'{student.first_name} {student.last_name}'
                final_attendence.append([usn, 'Present' if status else 'Absent', name, image])
        print(final_attendence)
        context = {
            'subject'    : subject,
            'sem'        : sem,
            'branch'     : branch,
            'division'   : division,
            'date'       : date,
            'attendence' : final_attendence,
        }  
    else :
        # print(request.META.HTTP_REFERER,'---------========-***')
        attendence       = StudentAttendenceBlock.objects.all().last()
        if attendence:
            print(attendence,'===')
            subject          = attendence.subject
            sem              = attendence.sem
            branch           = attendence.branch
            division         = attendence.division
            date             = attendence.date
            final_attendence = []
            attendence       = attendence.attendenceBlock['data']
            for usn, status in attendence.items():
                student = Student.objects.filter(student_usn = usn).first()
                image = student.image
                name  = f'{student.first_name} {student.last_name}'
                final_attendence.append([usn, 'Present' if status else 'Absent', name, image])
            context = {
                'subject'    : subject,
                'sem'        : sem,
                'branch'     : branch,
                'division'   : division,
                'date1'       : date,
                'attendence' : final_attendence,
            }  
            print(context)
        else :
            context = {}
    return render(request, template_name, context)
    
    