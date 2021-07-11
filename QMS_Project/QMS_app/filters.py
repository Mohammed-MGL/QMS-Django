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

    user__username = django_filters.CharFilter(
        field_name = 'user__username' ,
        lookup_expr='icontains',
        label='username' ,
        widget=forms.TextInput(attrs={'class': 'form-control  mb-4  ', 'placeholder' : 'Employee username'})
        )
    desk_num = CharFilter(field_name = 'desk_num' , lookup_expr= 'icontains',widget=forms.TextInput(attrs={'class': 'form-control  mb-4 ', 'placeholder' : 'Desk num Name'}),label ='') 
    Service = ModelChoiceFilter( queryset=ourService,field_name = 'Service' ,
    # empty_label="all Service" ,
    widget=forms.Select(attrs={'class': 'form-control mr-3  '}),label ='')
    
    class Meta:
       
        model = Employee
        # fields = '__all__'
        fields = ['desk_num','Service','user__username']


class UserFilter(django_filters.FilterSet):

    username = CharFilter(required = True ,field_name = 'username' , lookup_expr= 'icontains' ,widget=forms.TextInput(attrs={'class': 'form-control mx-3 mb-4 ', 'placeholder' : 'User name' ,'name':"username"} ),label ='') 
    first_name = CharFilter(field_name = 'first_name' , lookup_expr= 'icontains' ,widget=forms.TextInput(attrs={'class': 'form-control mx-3 mb-4 ', 'placeholder' : 'First name'} ),label ='') 
    last_name = CharFilter(field_name = 'last_name' , lookup_expr= 'icontains' ,widget=forms.TextInput(attrs={'class': 'form-control mx-3 mb-4 ', 'placeholder' : 'Last name'} ),label ='') 
   

    class Meta:
       
        model = User
        
        fields = ['username' , 'first_name' ,'last_name']
