from django.urls import path ,include 

from . import views
# from .views import *
from .apiViews import *
from rest_framework_simplejwt import views as jwt_views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

#koko
#Mohammed
urlpatterns = [
    # API endpoints 
    # account
    path('API/account/register/', RegisterView.as_view()),
    path('API/account/login/', TokenObtainPairView.as_view() ),
    # path('API/account/token/refresh/', TokenRefreshView.as_view() ),
    path('API/account/change_password/<int:pk>/', ChangePasswordView.as_view()),
    path('API/account/update_profile/<int:pk>/', UpdateProfileView.as_view()),
    # ServiceCenter
    path('API/allServiceCenter/',ServiceCenter.as_view(),),
    path('API/search/ServiceCenter/<str:name>',Search_ServiceCenter.as_view(), ),
    path('API/ServiceCenterDetails/<int:id>',ServiceCenterDetails.as_view(), ),
    # Service
    path('API/ServiceDetails/<str:SID>',ServiceDetails.as_view(), ),
    path('API/UserReservations/',UserReservations.as_view(), ),

    path('API/BookInService/<str:sID>',BookInService.as_view(), ),
    path('API/cancelBook/<str:BID>',cancelBook.as_view(), ),
    path('API/InCenter/<str:BID>',InCenter.as_view(), ),
    



    # web endpoints:
    path('login/',views.loginPage, name = 'login'),
    path('logout/',views.logoutUser, name = 'logout'),
    # dashboard
    path('dashboard/',views.dashboard, name = 'dashboard'),
    path('updatePassWord/',views.updatePassWord, name = 'updatePassWord'),

    # employee
    path('employees/',views.employees, name = 'employees'),
    path('addEmployee/',views.addEmployee, name = 'addEmployee'),
    path('viewEmployee/<str:eID>',views.viewEmployee, name = 'viewEmployee'),
    path('updateEmployee/<str:eID>',views.updateEmployee, name = 'updateEmployee'),
    path('updateEmployeePassWord/<str:eID>',views.updateEmployeePassWord, name = 'updateEmployeePassWord'),
    path('deleteEmployee/<str:eID>',views.deleteEmployee, name = 'deleteEmployee'),

    # service
    path('services/',views.services, name = 'services'),
    # path('addService/',views.addService, name = 'addService'),
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



    # employee template
    path('home',views.home, name = 'home'), 
   

    
    
]


    