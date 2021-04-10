from django.forms import ModelForm
from .models import Employee

class EmployeeForm(ModelForm):
    """Form definition for Employee."""

    class Meta:
        """Meta definition for Employeeform."""

        model = Employee
        fields = '__all__'

