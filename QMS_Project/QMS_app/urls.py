from django.urls import path ,include

from . import views
# from .views import *
from .apiViews import ServiceCenter_View , WorkTime_View ,Search_ServiceCenter

urlpatterns = [
    # API endpoints
    path('API/allServiceCenter',ServiceCenter_View.as_view(), ),
    path('API/WorkTime/<int:id>',WorkTime_View.as_view(), ),
    path('API/search/ServiceCenter/<str:name>',Search_ServiceCenter.as_view(), ),

    # web endpoints
    path('employees/',views.employees, name = 'employees'),
    path('createEmployee/',views.createEmployee, name = 'createEmployee'),
    path('updateEmployee/<str:eID>',views.updateEmployee, name = 'updateEmployee'),
    path('deleteEmployee/<str:eID>',views.deleteEmployee, name = 'deleteEmployee'),

    
    # path('Employee/<str:eID>',views.Employee, name = 'Employee'),


]

# from django.urls import path
# from . import views

# urlpatterns = [
#     path('black&white/',views.bwlist, name = 'index'),
#     path('services/',views.service, name = 'index'),
#     path('dashboard/',views.dash, name = 'dash'),  
#     path('dash/',views.d, name = 'd'),
#     path('Employee/',views.Employee, name = 'Emp'),
#     path('Editemployee/',views.Editemployee, name = 'Emp'),
#     path('addservice/',views.addservice, name = 'Emp'),]
    