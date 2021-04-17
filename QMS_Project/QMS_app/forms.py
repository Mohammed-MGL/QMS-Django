from django.forms import ModelForm
from .models import Employee , Service

from django import forms


class EmployeeForm(ModelForm):
    """Form definition for Employee."""

    class Meta:
        """Meta definition for Employeeform."""

        model = Employee
        fields = ['name','desk_num','username','phone','Service','location']

        widgets = {
            'name' : forms.TextInput(attrs={'class': 'form-control mb-4 '}),
            'desk_num' : forms.TextInput(attrs={'class': 'form-control mb-4'}),
            'username' : forms.TextInput(attrs={'class': 'form-control mb-4 '}),
            'phone' : forms.TextInput(attrs={'class': 'form-control mb-4 '}),
            
            'location' : forms.TextInput(attrs={'class': 'form-control mb-4'}),
        }


class ServiceForm(ModelForm):
    """Form definition for Employee."""

    class Meta:
        """Meta definition for Employeeform."""

        model = Service
        fields = '__all__'

        widgets = {
            'name' : forms.TextInput(attrs={'class': 'input', 'placeholder' : 'Your Name'}),
        }



 

             