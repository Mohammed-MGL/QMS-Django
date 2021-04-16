from django.forms import ModelForm
from .models import Employee , Service

from django import forms


class EmployeeForm(ModelForm):
    """Form definition for Employee."""

    class Meta:
        """Meta definition for Employeeform."""

        model = Employee
        fields = '__all__'

        widgets = {
            'name' : forms.TextInput(attrs={'class': 'input', 'placeholder' : 'Your Name'}),
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