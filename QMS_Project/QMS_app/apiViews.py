from django.shortcuts import render

# Create your views here.
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import *
from .models import Service_center

class ServiceCenter_View(APIView):
    def get(self , request , *args ,**kwargs):
        qs = Service_center.objects.all()
        serializer = Service_centerSerializer(qs,many=True)
        return Response(serializer.data)

    # def post(self , request , *args ,**kwargs):
    #     serializer = Service_centerSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data)
    #     return Response(serializer.error)


class WorkTime_View(APIView):
    def get(self , request ,id, *args ,**kwargs):
        qs = Work_time.objects.get(id = id )
        serializer = Work_timeSerializer(qs)
        return Response(serializer.data)
    
class Search_ServiceCenter(APIView):
    def get(self , request ,name, *args ,**kwargs):
        
        qs = Service_center.objects.filter(name__icontains=name)
        num = qs.__len__()
        serializer = Service_centerSerializer(qs , many = True)
        content = {
            'pageTotal' : num,
            'pagenum' : num,
            'results' : serializer.data,
        }
        return Response(content)