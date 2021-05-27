from django.http.response import JsonResponse
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
from .models import Service_center , User ,Service
from rest_framework.permissions import IsAuthenticated
from django.core.serializers import json
from django.utils import timezone

    # UserServics

    
class UserReservations(ListAPIView):
    permission_classes = (IsAuthenticated,)
    
    def get_queryset(self):
        user = self.request.user
        return Service_Record.objects.filter(user = user ,is_accept = True ,is_served = False ,is_cancelled =False)

    pagination_class = CustomPagination
    serializer_class = ReservationsSerializer
# class UserReservations(APIView):
#     permission_classes = (IsAuthenticated,)
#     pagination_class = CustomPagination

    
#     def get(self , request , *args ,**kwargs):
#         user = request.user

#         qs = Service_Record.objects.filter(user = user ,is_accept = True ,is_served = False ,is_cancelled =False)

#         class UserR:
#             sid = None
#             SCname   = None
#             Sname  = None

#             def __init__(self,sid,SCname  , Sname):
#                 self.name = sid
#                 self.SCname = SCname
#                 self.Sname = Sname

#         sdList = [] 

#         for s in qs:
#             sid = s.id
#             SCname = s.Service.Service_center
#             Sname = s.Service.name
#             sd = UserR(sid,SCname , Sname)
        
#             sdList.append(sd)
#         print(sdList)
#         json_serializer = json.Serializer()
#         json_serialized = json_serializer.serialize(sdList)
#         # SC_serializer =Service_center_detailSerializer(x ,many= False) 
#         # w = Work_time.objects.get(Service_center= id)
#         # w_serializer = Work_timeSerializer(w ,many= False)
#         # y = Service.objects.filter(Service_center= id).order_by('name')
#         # S_serializer = ServiceSerializer(y ,many= True) 
#         content = {
#             # 'service_center' : SC_serializer.data,
#             # 'work_time' :    w_serializer.data ,
#             # 'services' :  S_serializer.data ,  
#         } 
#         return Response(json_serialized)  


class ServiceCenter(ListAPIView):
    permission_classes = (IsAuthenticated,)
    # queryset = Service_center.objects.all() 
    queryset = Service_center.objects.order_by('name')
    pagination_class = CustomPagination
    serializer_class = Service_centerListSerializer

# class UserCreate(generics.CreateAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
#     permission_classes = (AllowAny, )


class Search_ServiceCenter(ListAPIView):
    permission_classes = (IsAuthenticated,)
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
        SC_serializer =Service_center_detailSerializer(x ,many= False , context={'request': request}) 
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
        
        user =request.user
        service =Service.objects.get(id = sID)
    
        sr =  Service_Record.objects.filter(user = user ,Service = service ,is_accept = True ,is_served = False ,is_cancelled =False)
        if (sr):
            return Response({'Accepted':False }) 

        is_userBlocked = Black_list.objects.filter(user= user ,Service_center = service.Service_center )
        if is_userBlocked:
            Service_Record.objects.create(Service=service , user=user , is_accept= False )
            return Response({'Accepted':False })
                
        book = Service_Record.objects.create(Service=service , user=user, IS_InCenter = False ,  Queue_type = 'B' )
        return Response({'Accepted':True }) 

class  cancelReservation(APIView):
    permission_classes = (IsAuthenticated,)
    
    
    def post(self , request ,sID, *args ,**kwargs):
        
        user =request.user
        service =Service.objects.get(id = sID)
        is_inQ = False
        book =  Service_Record.objects.filter(user = user ,Service = service ,is_accept = True ,is_served = False ,is_cancelled =False).first()
        if(book):

            book.O_Time = timezone.now().strftime("%Y-%m-%d %H:%M:%S") 
            book.is_cancelled = True
            # print(book)
            book.save()

            is_inQ = True

            return Response({ 'Accepted': True }) 
        else:
            return Response({ 'Accepted': False }) 


class  UserInCenter(APIView):
    permission_classes = (IsAuthenticated,)
    
    
    def post(self , request ,sID, *args ,**kwargs):
        
        user =request.user
        
        
        service =Service.objects.get(id = sID)
        book =  Service_Record.objects.filter(user = user ,Service = service ,is_accept = True ,is_served = False ,is_cancelled =False).last()
        if(book):

            book.IS_InCenter = True
            book.save()

            return Response({ 'Accepted': True })

        else:
            return Response({ 'Accepted': False }) 
        



class  ServiceDetails(APIView ):
    permission_classes = (IsAuthenticated,)
    
    
    def get(self , request ,SID, *args ,**kwargs):
        
        user =request.user
        service =Service.objects.get(id = SID) 
        serviceName = service.name
        queue = Service_Record.objects.filter(Service=service ,is_accept =True ,is_served= False ,is_cancelled= False ,Queue_type = 'B' )
        userReservation= Service_Record.objects.filter(Service=service ,is_accept =True ,is_served= False ,is_cancelled= False ,user= user ).first()
        
        if(userReservation is None):
            is_inQ =  False
        else:
            is_inQ =  True


        if (is_inQ):
            queue = queue.filter(IQ_Time__lte=userReservation.IQ_Time)

        queueCount = queue.count()
        waitingTime = "5 min"




        
        return Response({
            "id" : service.id,
            "name" : serviceName,
            "queueCount" : queueCount,
            "waitingTime" : waitingTime,
            "is_inQ" : is_inQ,
        }) 





class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer



class ChangePasswordView(generics.UpdateAPIView):

    queryset = User.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = ChangePasswordSerializer
        

class UpdateProfileView(generics.UpdateAPIView):

    queryset = User.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = UpdateUserSerializer        




 
class Profile(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self , request , *args ,**kwargs):

        user =  request.user
        user_serializer = UserSerializer(user ,many= False)
    
        return Response(user_serializer.data)




class UserHistory(ListAPIView):
    permission_classes = (IsAuthenticated,)
    
    def get_queryset(self):
        user = self.request.user
        serviceRecords = Service_Record.objects.filter(user = user ,is_served = True)
        qs2 = Service_Record.objects.filter(user = user ,is_cancelled = True)
        qs3 = Service_Record.objects.filter(user = user ,is_accept = False)
        serviceRecords = serviceRecords.union(qs2,qs3)
        serviceRecords = serviceRecords.order_by('IQ_Time')
        return serviceRecords

    pagination_class = CustomPagination
    serializer_class = HistorySerializer

  