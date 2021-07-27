
from .models import *
from django.utils import timezone
import math
from datetime import timedelta, date, time, datetime 


def update_something():
    print("this function runs every 1 min "+ timezone.now().strftime("%Y-%m-%d %H:%M:%S.%f"))
    update_service_time()

def update_service_time():
    services = Service.objects.all()
    for ser in services:

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
                return

            minutes = math.ceil(avrageServingTime / 60)

            # avrageServingTime = timedelta(seconds=avrageServingTime)

            ser.time = minutes
            
            ser.save()


