import django_filters

from django_filters import CharFilter

from django import forms 

from .models import *


class EmployeeFilter(django_filters.FilterSet):

    name = CharFilter(field_name = 'name' , lookup_expr= 'icontains' ,widget=forms.TextInput(attrs={'class': 'form-control mx-3 mb-4 ', 'placeholder' : 'Employee Name'} ),label ='') 
    desk_num = CharFilter(field_name = 'desk_num' , lookup_expr= 'icontains',widget=forms.TextInput(attrs={'class': 'form-control mx-3 mb-5  ', 'placeholder' : 'Desk num Name'}),label ='') 
    # Service = ChoiceFilter(field_name = 'Service' , lookup_expr= 'icontains',widget=forms.Select(attrs={'class': '', 'placeholder' : 'Desk num Name'}),label ='') 
    
    class Meta:
       
        model = Employee
        # fields = '__all__'
        fields = ['name', 'desk_num','Service']
