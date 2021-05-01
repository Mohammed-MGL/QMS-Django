from django.urls import path ,include 

from . import views
# from .views import *
from .apiViews import *

#koko
#Mohammed
urlpatterns = [
    # API endpoints 
    path('API/allServiceCenter/',ServiceCenter.as_view(),),
    path('API/search/ServiceCenter/<str:name>',Search_ServiceCenter.as_view(), ),
    path('API/ServiceCenterDetails/<int:id>',ServiceCenterDetails.as_view(), ),
    path('account/register/', UserCreate.as_view()),
    path('API/BookInService/<str:sID>',BookInService.as_view(), ),
    path('API/CansleBook/<str:sID>',BookInService.as_view(), ),

    path('login/',views.loginPage, name = 'login'),
    path('logout/',views.logoutUser, name = 'logout'),

    # web endpoints:
    # dashboard
    path('dashboard/',views.dashboard, name = 'dashboard'),
    # employee
    path('employees/',views.employees, name = 'employees'),
    path('addEmployee/',views.addEmployee, name = 'addEmployee'),
    path('viewEmployee/<str:eID>',views.viewEmployee, name = 'viewEmployee'),
    path('updateEmployee/<str:eID>',views.updateEmployee, name = 'updateEmployee'),
    path('updateEmployeePassWord/<str:eID>',views.updateEmployeePassWord, name = 'updateEmployeePassWord'),
    path('deleteEmployee/<str:eID>',views.deleteEmployee, name = 'deleteEmployee'),

    # service
    path('services/',views.services, name = 'services'),
    path('addService/',views.addService, name = 'addService'),
    path('viewService/<str:sID>',views.viewService, name = 'viewService'),
    path('editService/<str:sID>',views.editService, name = 'editService'),
    path('deleteService/<str:sID>',views.deleteService, name = 'deleteService'),
    path('serviceChangeState/<str:sID>',views.serviceChangeState, name = 'serviceChangeState'),

    # Black_list & White_list
    path('black&whiteList/',views.bwlist, name = 'bwlist'),
    path('deleteUserFromBL/<str:uID>',views.deleteUserFromBL, name = 'deleteUserFromBL'),
    path('deleteUserFromWL/<str:uID>',views.deleteUserFromWL, name = 'deleteUserFromWL'),
    path('serachForUser',views.serachForUser, name = 'serachForUser'),
    path('addToBlackLIst/<str:uID>',views.addToBlackLIst, name = 'addToBlackLIst'),
    path('addToWhiteLIst/<str:uID>',views.addToWhiteLIst, name = 'addToWhiteLIst'),
    

    path('BookAsGuest/<str:scID>',views.BookAsGuest, name = 'BookAsGuest'), 
    
    path('book_in_service/<str:sID>',views.book_in_service, name = 'book_in_service'),
    path('ServiceCnterProfile',views.ServiceCnterProfile, name = 'ServiceCnterProfile'),
    
    
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
    