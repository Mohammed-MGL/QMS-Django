from django.conf.urls import include
from django.urls import path  

from . import apiViews
from rest_framework_simplejwt import views as jwt_views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from fcm_django.api.rest_framework import FCMDeviceAuthorizedViewSet


urlpatterns = [
    # API endpoints
    # account
    path('account/register/', apiViews.RegisterView.as_view()),
    path('account/login/', TokenObtainPairView.as_view()),
    path('account/profile/', apiViews.Profile.as_view()),
    path('account/register/FCMtoken/', FCMDeviceAuthorizedViewSet.as_view({'post': 'create'}), name='create_fcm_device'),
    # path('account/token/refresh/', TokenRefreshView.as_view() ),
    path('account/change_password/', apiViews.ChangePasswordView.as_view()),
    path('account/update_profile/<int:pk>/', apiViews.UpdateProfileView.as_view()),
    # ServiceCenter
    path('allServiceCenter/',apiViews.ServiceCenter.as_view(),),
    path('search/ServiceCenter/<str:name>',apiViews.Search_ServiceCenter.as_view(),),
    path('ServiceCenterDetails/<int:id>',apiViews.ServiceCenterDetails.as_view(),),
    path('ServiceCenterDetailsByName/<str:name>',apiViews.ServiceCenterDetailsByName.as_view(),),
    # Service
    path('ServiceDetails/<str:SID>',apiViews.ServiceDetails.as_view(), ),
    path('UserReservations/',apiViews.UserReservations.as_view(), ),
    path('UserHistory/', apiViews.UserHistory.as_view() ),

    path('BookInService/<str:sID>',apiViews.BookInService.as_view(), ),
    path('CancelReservation/<str:sID>',apiViews.cancelReservation.as_view(), ),
    path('UserInCenter/<str:sID>',apiViews.UserInCenter.as_view(), ),
    
]


    