from django.shortcuts import render

# Create your views here.
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from rest_framework import generics

from rest_framework.generics import ListAPIView
from QMS_Project.pagination import CustomPagination
from rest_framework.permissions import IsAuthenticated  , AllowAny

from .serializers import *
from .models import Service_center

class ServiceCenter(ListAPIView):
    # permission_classes = (IsAuthenticated,)
    queryset = Service_center.objects.all() 
    queryset = Service_center.objects.order_by('name')
    pagination_class = CustomPagination
    serializer_class = Service_centerListSerializer

class UserCreate(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny, )


class Search_ServiceCenter(ListAPIView):
    
    pagination_class = CustomPagination
    serializer_class = Service_centerListSerializer

    model = serializer_class.Meta.model
    def get_queryset(self):
        name = self.kwargs['name']
        queryset = self.model.objects.filter(name__istartswith=name)
        qs2 = self.model.objects.filter(name__icontains=name)
        qs3 = self.model.objects.filter(name__iendswith=name)
        queryset = queryset.union(qs2,qs3)
        return queryset

# class ServiceCenter_View(APIView):
#     def get(self , request , *args ,**kwargs):
#         qs = Service_center.objects.all()
#         serializer = Service_centerSerializer(qs,many=True)
#         return Response(serializer.data)

    # def post(self , request , *args ,**kwargs):
    #     serializer = Service_centerSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data)
    #     return Response(serializer.error)


# class WorkTime_View(APIView):
#     def get(self , request ,id, *args ,**kwargs):
#         qs = Work_time.objects.get(id = id )
#         serializer = Work_timeSerializer(qs)
#         return Response(serializer.data)
    
# class Search_ServiceCenter(APIView):
#     def get(self , request ,name, *args ,**kwargs):
        
#         qs = Service_center.objects.filter(name__icontains=name)
#         num = qs.__len__()
#         serializer = Service_centerListSerializer(qs , many = True)
#         content = {
#             'pageTotal' : num,
#             'pagenum' : num,
#             'results' : serializer.data,
#         }
#         return Response(content)


class ServiceCenterDetails(APIView):
    permission_classes = (IsAuthenticated,)
    
    
    def get(self , request ,id, *args ,**kwargs):
        x = Service_center.objects.get(id=id)
        SC_serializer =Service_center_detailSerializer(x ,many= False) 
        w = Work_time.objects.get(Service_center= id)
        w_serializer = Work_timeSerializer(w ,many= False)
        y = Service.objects.filter(Service_center= id).order_by('name')
        S_serializer = ServiceSerializer(y ,many= True) 
        content = {
            'service_center' : SC_serializer.data,
            'work_time' :    w_serializer.data ,
            'services' :  S_serializer.data ,  
        } 
        return Response(content)  


class  BookInService(APIView):
    permission_classes = (IsAuthenticated,)
    
    
    def post(self , request ,sID, *args ,**kwargs):
        service =Service.objects.get(id = sID)
        user =request.user
        book = Service_Record.objects.create(Service=service , user=user, IS_InCenter = False ,  Queue_type = 'B' )
        return Response({'Accepted':True}) 

class  CansleBook(APIView):
    permission_classes = (IsAuthenticated,)
    
    
    def post(self , request ,BID, *args ,**kwargs):
        
        user =request.user
        book = Service_Record.objects.get(id= BID)
        
        return Response({'Accepted':True}) 
        



