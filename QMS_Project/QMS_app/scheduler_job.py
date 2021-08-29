
from .models import *
from django.utils import timezone
import math
from datetime import timedelta, date, time, datetime 
from firebase_admin.messaging import Message ,Notification
from fcm_django.models import FCMDevice 

def update_something():
    print("this function runs every 1 min "+ timezone.now().strftime("%Y-%m-%d %H:%M:%S.%f"))


def update_service_time():
    print("update_service_time")
    services = Service.objects.all()
    print(services)
    for ser in services:
        print(ser)

        if ser.IS_static==True:

            ser.time = ser.defaultTime
            ser.save()
          

        else:
            

            today_min = datetime.combine(timezone.now().date(), datetime.today().time().min)
            today_max = datetime.combine(timezone.now().date(), datetime.today().time().max)
            
            todayRecord = Service_Record.objects.filter(
                Service = ser  ,
                is_served = True,
                P_Time__range=(today_min, today_max)        
                )

        

            totalServingTime = 0
            avrageServingTime = 0 
            

            if todayRecord:
                for i in todayRecord:

                    servingTime  = i.O_Time - i.P_Time 
                    totalServingTime += servingTime.seconds

                avrageServingTime =  math.ceil(totalServingTime / todayRecord.count())
            else:   
                ser.time = ser.defaultTime
                ser.save()
                continue

            minutes = math.ceil(avrageServingTime / 60)

            # avrageServingTime = timedelta(seconds=avrageServingTime)

            ser.time = minutes
   
            ser.save()


def delete_old_book():
    print("cancel")
    q = Service_Record.objects.filter(status ='A' ,is_served= False ,is_cancelled= False  ,IS_InCenter= False  )
    q = Service_Record.objects.filter(status ='A' ,is_served= False ,is_cancelled= False  ,IS_InCenter= False  )
    q2 = Service_Record.objects.filter(status ='P' ,is_served= False ,is_cancelled= False  ,IS_InCenter= False  )
    q = q.union(q2)
    for book in q:
        book.status ='R'
        book.save()
        device = FCMDevice.objects.filter(User=book.user).first()
        
        device.send_message(Message(
        notification=Notification("Servies Center : book rejected", body="The service center has been closed",
        image="https://149351115.v2.pressablecdn.com/wp-content/uploads/2020/02/iStock-1163542789.jpg" )))


           

