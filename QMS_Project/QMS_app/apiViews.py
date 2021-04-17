from django.shortcuts import render

# Create your views here.
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListAPIView
from QMS_Project.pagination import CustomPagination

from .serializers import *
from .models import Service_center

class ServiceCenter_View(ListAPIView):
    # queryset = Service_center.objects.all().
    queryset = Service_center.objects.order_by('name')
    pagination_class = CustomPagination
    serializer_class = Service_centerListSerializer


class Search_ServiceCenter(ListAPIView):
    # queryset = Service_center.objects.all().
    pagination_class = CustomPagination
    serializer_class = Service_centerListSerializer

    model = serializer_class.Meta.model
    def get_queryset(self):
        name = self.kwargs['name']
        queryset = self.model.objects.filter(name__icontains=name).order_by('name')
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
