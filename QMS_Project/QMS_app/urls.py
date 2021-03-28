from django.urls import path ,include
from . import views
# from .views import *
from .apiViews import ServiceCenter_View , WorkTime_View ,Search_ServiceCenter

urlpatterns = [
    # API endpoints
    path('api/allServiceCenter',ServiceCenter_View.as_view(), ),
    path('api/WorkTime/<int:id>',WorkTime_View.as_view(), ),
    path('api/search/ServiceCenter/<str:name>',Search_ServiceCenter.as_view(), ),

]

   
    