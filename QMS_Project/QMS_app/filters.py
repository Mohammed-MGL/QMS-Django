import django_filters

from django_filters import CharFilter , ModelChoiceFilter

from django import forms 

from .models import *



def ourService(request):
    if request is None:
        return Service.objects.none()

    sc = Manager.objects.get(user = request.user).Service_center
    return Service.objects.filter(Service_center = sc.id)


class EmployeeFilter(django_filters.FilterSet):

    desk_num = CharFilter(field_name = 'desk_num' , lookup_expr= 'icontains',widget=forms.TextInput(attrs={'class': 'form-control mx-3 mb-5  ', 'placeholder' : 'Desk num Name'}),label ='') 
    Service = ModelChoiceFilter( queryset=ourService,field_name = 'Service' ,widget=forms.Select(attrs={'class': 'form-control mx-3 mb-4 ', 'placeholder' : 'Desk num Name'}),label ='')
    
    user__username = django_filters.CharFilter(field_name = 'user__username' ,lookup_expr='icontains', label='username' ,widget=forms.TextInput(attrs={'class': 'form-control mx-3 mb-5  ', 'placeholder' : 'Employee username'}))

    class Meta:
       
        model = Employee
        # fields = '__all__'
        fields = ['desk_num','Service','user__username']


class UserFilter(django_filters.FilterSet):

    username = CharFilter(field_name = 'username' , lookup_expr= 'icontains' ,widget=forms.TextInput(attrs={'class': 'form-control mx-3 mb-4 ', 'placeholder' : 'User name'} ),label ='') 
    first_name = CharFilter(field_name = 'first_name' , lookup_expr= 'icontains' ,widget=forms.TextInput(attrs={'class': 'form-control mx-3 mb-4 ', 'placeholder' : 'First name'} ),label ='') 
    last_name = CharFilter(field_name = 'last_name' , lookup_expr= 'icontains' ,widget=forms.TextInput(attrs={'class': 'form-control mx-3 mb-4 ', 'placeholder' : 'Last name'} ),label ='') 
   

    class Meta:
       
        model = User
        
        fields = ['username' , 'first_name' ,'last_name']
