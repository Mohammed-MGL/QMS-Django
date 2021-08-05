from django.forms import ModelForm
from .models import *
from django.db import transaction
from django import forms
from django.contrib.auth.forms import UserCreationForm , PasswordChangeForm


class EmployeeCreationForm(UserCreationForm):
    Fist_Name = forms.CharField(required = False , widget=forms.TextInput(attrs={'class': 'form-control mb-4 ml-2  '}))
    Last_Name = forms.CharField(required = False , widget=forms.TextInput(attrs={'class': 'form-control mb-4 ml-2 '}  ))
    Service = forms.ModelChoiceField(queryset=Service.objects.all(), widget=forms.Select(attrs={'class': 'form-control mb-4 ml-2  '}))
    desk_num = forms.CharField(required = False , widget=forms.TextInput(attrs={'class': 'form-control mb-4 ml-2 mt-4'}  ) )
    notes = forms.CharField(required = False , widget=forms.TextInput(attrs={'class': 'form-control mb-4 ml-2  '} ) )
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control mb-4 ml-2 '}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control mb-4 ml-2 '}))
    
    osc = None

    def __init__(self, sc, *args, **kwargs):
        super(EmployeeCreationForm, self).__init__(*args, **kwargs)
        self.fields['Service'].queryset = Service.objects.filter(Service_center = sc.id)
        self.fields['password1'].label = "Password"
        self.fields['password2'].label = "Confirm Password"  
        self.osc = sc

    class Meta(UserCreationForm.Meta):
        model = User

        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control mb-4 ml-2'}),
        }

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_employee = True
        user.save()
        employee = Employee.objects.create(user=user,Service_center = self.osc,Service= self.cleaned_data['Service'] ,desk_num = self.cleaned_data['desk_num'],notes = self.cleaned_data['notes'] )
        return user

class PasswordChangeForm(PasswordChangeForm):
        
    def __init__(self, *args, **kwargs):
        super(PasswordChangeForm, self).__init__(*args, **kwargs)
        
        self.fields['old_password'].widget = forms.PasswordInput(attrs={'class': 'form-control mb-4 ml-2 '})
        self.fields['new_password1'].widget = forms.PasswordInput(attrs={'class': 'form-control mb-4 ml-2 '})
        self.fields['new_password2'].widget = forms.PasswordInput(attrs={'class': 'form-control mb-4 ml-2 '})

class EmployeeForm(ModelForm):
    """Form definition for Employee."""

    def __init__(self, sc, *args, **kwargs):
        super(EmployeeForm, self).__init__(*args, **kwargs)
        self.fields['Service'].queryset = Service.objects.filter(Service_center = sc.id)

    class Meta:
        """Meta definition for Employeeform."""

        model = Employee
        fields = ['Service','desk_num','notes']

        widgets = {
            'Service' : forms.Select(attrs={'class': 'form-control mb-4 '}),
            'desk_num' : forms.TextInput(attrs={'class': 'form-control mb-4'}),
            'notes' : forms.TextInput(attrs={'class': 'form-control mb-4 '}),
            
        }


class ServiceForm(ModelForm):

    osc = None

    def __init__(self, sc, *args, **kwargs):
        super(ServiceForm, self).__init__(*args, **kwargs)
        self.osc = sc 


    class Meta:

        model = Service
        fields = ['name' , 'IS_Active','defaultTime','IS_static' ]

        widgets = {
            'name' : forms.TextInput(attrs={'class': 'form-control mb-4', 'placeholder' : 'Add service name '}),
            'defaultTime' : forms.TextInput(attrs={'class': 'form-control mb-4', 'placeholder' : 'Add default time '}),
            # 'IS_Active' : forms.CheckboxInput(attrs={'class': 'form-check-input', 'placeholder' : 'Your Name'}),
        }

    @transaction.atomic
    def save(self):
        Service = super().save(commit=False)
        Service.Service_center = self.osc
        
        Service.time = Service.defaultTime
            
        Service.save()
        return Service


class scform(forms.ModelForm): 
    name = forms.CharField(required = False , widget=forms.TextInput(attrs={'class': 'form-control  ml-2  '}))
    location = forms.CharField(required = False , widget=forms.TextInput(attrs={'class': 'form-control  ml-2 '}  ))
    
    phone = forms.CharField(required = False , widget=forms.TextInput(attrs={'class': 'form-control  ml-2 mt-1'}  ) )
    mapLocations = forms.CharField(required = False , widget=forms.TextInput(attrs={'class': 'form-control  ml-2  '}  ),label="Map Location")
    
    # Image = forms.ImageField(required = False , widget=forms.choices(attrs={'class': 'form-control mb-4 ml-2 '}  ))
    # Icon = forms.ImageField(required = False , widget=forms.TextInput(attrs={'class': 'form-control mb-4 ml-2 '}  ))
    # QR = forms.ImageField(required = False , widget=forms.TextInput(attrs={'class': 'form-control mb-4 ml-2 '}  ))
    
    
    class Meta: 
        model = Service_center 
        fields = ['name','location','mapLocations','phone','Image','Icon','QR']




class MoveCustomerForm(ModelForm):
    """Form definition for Employee."""
    Service = forms.ModelChoiceField(queryset=Service.objects.all(), widget=forms.Select(attrs={'class': 'form-control mb-4 ml-2  '}))

    osc = None

    def __init__(self, sc, *args, **kwargs):
        super(MoveCustomerForm, self).__init__(*args, **kwargs)
        self.fields['Service'].queryset = Service.objects.filter(Service_center = sc.id,IS_Active= True)
        self.osc = sc 


    class Meta:
        """Meta definition for Employeeform."""

        model = Service_Record
        fields = ['Service']

        widgets = {
            'Service' : forms.Select(attrs={'class': 'form-control mb-4 '}),
            # 'IS_Active' : forms.CheckboxInput(attrs={'class': 'form-check-input', 'placeholder' : 'Your Name'}),
        }

    # @transaction.atomic
    # def save(self):
    #     Service = super().save(commit=False)
    #     Service.Service_center = self.osc
    #     Service.save()
    #     return Service
        

