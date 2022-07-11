
from django.views.generic import TemplateView
from django.urls import path
from home.views import *
from home import views as v
from django.contrib.auth.decorators import login_required


urlpatterns = [
    path('login_admin/', v.login_page, name = 'login_admin'),
    path('login_faculty/', v.login_page, name = 'login_faculty'),
    path('login_student/', v.login_page, name = 'login_student'),
    path('', HomPage.as_view(), name = 'home'),
    path('home/', HomPage.as_view(), name = 'home'),
    path('register/', login_required(RegisterPage.as_view()), name = 'register'),
    path('register_student/', login_required(RegisterStudentPage.as_view()), name = 'register_student'),
    path('update_faculty/<int:pk>', login_required(UpdateFaculty.as_view()), name = 'update_faculty'),
    path('update_student/<int:pk>', login_required(UpdateStudent.as_view()), name = 'update_student'),
    path('delete_faculty/<int:pk>', login_required(DeleteFaculty.as_view()), name = 'delete_faculty'),
    path('delete_student/<int:pk>', login_required(DeleteStudent.as_view()), name = 'delete_student'),
    path('faculties/', login_required(login_required(FacultiesPage.as_view())), name = 'faculties'),
    path('students1/', login_required(StudentLis1t1.as_view()), name = 'students1'),
    path('Student_attendence_credentials/', login_required(StudentAttendenceCredentials.as_view()), name = 'Student_attendence_credentials'),
    path('student_attendenct/', login_required(v.student_attendence), name = 'student_attendenct'),
    # path('student_attendenct/', login_required(StudentAttendence.as_view()), name = 'student_attendenct'),
    path('student_details/<int:pk>', login_required(StudentDetails.as_view()), name = 'student_details'),
    path('facultyt_details/<int:pk>', login_required(FacultytDetails.as_view()), name = 'facultyt_details'),
    path('create_faculty_user/<int:pk>', login_required(create_user), name = 'create_faculty_user'),
    path('create_student_user/<int:pk>', login_required(create_user), name = 'create_student_user'),
    path('logout/', v.lgout, name = 'logout'),
    path('forgot_password/', ForgotPassword.as_view(), name = 'forgot_password'),
    path('download_student_attendence/<int:pk>', v.download_student_details, name = 'download_student_attendence'),
    path('attendence_overview/', attendence_overview, name = 'attendence_overview'),
    path('send_message/<int:pk>', send_message, name = 'send_message'),
]

