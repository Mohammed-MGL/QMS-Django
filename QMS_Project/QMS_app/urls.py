from django.urls import path ,include

from . import views
# from .views import *
from .apiViews import ServiceCenter_View , WorkTime_View ,Search_ServiceCenter

urlpatterns = [
    # API endpoints
    path('API/allServiceCenter',ServiceCenter_View.as_view(),),
    path('API/search/ServiceCenter/<str:name>',Search_ServiceCenter.as_view(), ),
    path('API/WorkTime/<int:id>',WorkTime_View.as_view(),),
    path('API/ServiceCenterDetails/<int:id>',ServiceCenterDetails.as_view(), ),

    # web endpoints:
    # dashboard
    path('dashboard/',views.dashboard, name = 'dashboard'),
    # employee
    path('employees/',views.employees, name = 'employees'),
    path('addEmployee/',views.addEmployee, name = 'addEmployee'),
    path('viewEmployee/<str:eID>',views.viewEmployee, name = 'viewEmployee'),
    path('updateEmployee/<str:eID>',views.updateEmployee, name = 'updateEmployee'),
    path('deleteEmployee/<str:eID>',views.deleteEmployee, name = 'deleteEmployee'),

    # service
    path('services/',views.services, name = 'services'),
    path('addService/',views.addService, name = 'addService'),
    path('viewService/<str:sID>',views.viewService, name = 'viewService'),
    path('editService/<str:sID>',views.editService, name = 'editService'),
    path('deleteService/<str:sID>',views.deleteService, name = 'deleteService'),

    # Black_list & White_list
    path('black&whiteList/',views.bwlist, name = 'bwlist'),
    path('deleteUserFromBL/<str:uID>',views.deleteUserFromBL, name = 'deleteUserFromBL'),
    path('deleteUserFromWL/<str:uID>',views.deleteUserFromWL, name = 'deleteUserFromWL'),
    




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
    