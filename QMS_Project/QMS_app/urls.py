from django.urls import path  

from . import views


urlpatterns = [
    
    path('login/',views.loginPage, name = 'login'),
    path('logout/',views.logoutUser, name = 'logout'),
    # dashboard
    path('dashboard/',views.dashboard, name = 'dashboard'),
    path('ManagerProfile/',views.ManagerProfile, name = 'ManagerProfile'),
    path('SendMessage/<str:ID>/<str:MSG>/', views.SendMessageView , name="send_message") ,
    path('servicecenterChangeState',views.scChangeState, name = 'scChangeState'),
    path('servicecenterChangeAutoAccept',views.scChangeAutoAccept, name = 'scChangeAutoAccept'),
    path('acceptUser/<str:ID>',views.acceptUser, name = 'acceptUser'),
    path('rejectUser/<str:ID>',views.rejectUser, name = 'rejectUser'),

    
    
 

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
    path('black&whiteList/',views.black_WhiteList, name = 'black_WhiteList'),
    path('deleteUserFromBL/<str:uID>',views.deleteUserFromBL, name = 'deleteUserFromBL'),
    path('deleteUserFromWL/<str:uID>',views.deleteUserFromWL, name = 'deleteUserFromWL'),
    path('serachForUser',views.serachForUser, name = 'serachForUser'),
    path('addToBlackLIst/<str:uID>',views.addToBlackLIst, name = 'addToBlackLIst'),
    path('addToWhiteLIst/<str:uID>',views.addToWhiteLIst, name = 'addToWhiteLIst'),
    path('systemBlackList/',views.systemBlackList, name = 'systemBlackList'),
    path('copysystemBlackList/',views.copysystemBlackList, name = 'copysystemBlackList'),
    
    

    path('BookInServiceCenter/<str:scID>',views.BookInServiceCenter, name = 'BookInServiceCenter'), 
    path('BookInService/<str:sID>',views.BookInService, name = 'BookInService'),
    path('ServiceCnterProfile',views.ServiceCnterProfile, name = 'ServiceCnterProfile'),



    # employee template
    path('home',views.home, name = 'home'),

]