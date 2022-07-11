from tkinter import Widget
from django import forms
from .models import Faculty

class FacultyForm(forms.ModelForm):
    
    class Meta:
        model = Faculty
        fields = ('first_name', 'last_name', 'date_of_birth', 'date_of_joining', 'email', 'gender', 'branch')

        # widgets = {
        #     'first_name' : forms.TextInput(attrs={'class':'form-control'}),
        #     'last_name' : forms.TextInput(attrs={'class':'form-control'}),
        #     'date_of_birth' : forms.DateField(attrs={'class':'form-control'}),
        #     'date_of_joining' : forms.DateField(attrs={'class':'form-control'}),
        #     'email' : forms.EmailField(attrs={'class':'form-control'}),
        #     'gender' : forms.Select(attrs={'class':'form-control'}),
        #     'branch' : forms.Select(attrs={'class':'form-control'}),
        # }