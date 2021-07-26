from django.db import models
from django.contrib.auth.models import User , AbstractUser
from django.utils import  timezone

from django.db.models.signals import post_save
from django.dispatch import receiver
import pyqrcode
import png
from pyqrcode import QRCode
import qrcode
from io import BytesIO
from django.core.files import File
from PIL import Image, ImageDraw
from django.contrib.auth import get_user_model



class User(AbstractUser):
    is_employee = models.BooleanField(default=False)
    is_manager = models.BooleanField(default=False)
    is_guest = models.BooleanField(default=False)


class Manager(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    Service_center = models.ForeignKey('Service_center', on_delete=models.CASCADE)

    def __str__(self):
        """String for representing the Model object."""
        return self.user.username + ' (' + self.Service_center.name+')'

class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    Service_center = models.ForeignKey('Service_center', on_delete=models.CASCADE)
    Service = models.ForeignKey('Service', on_delete=models.SET_NULL, null=True)
    desk_num = models.CharField(max_length=50 , blank=True)
    notes =  models.CharField(max_length=1000 , blank=True)

    class Meta:
        unique_together = ('Service_center', 'desk_num',)

    def __str__(self):
        """String for representing the Model object."""
        return self.user.username  

class Service_center(models.Model):
    name = models.CharField(max_length=300 , unique=True)
    location = models.CharField(max_length=500 , blank=True)
    mapLocations = models.CharField(max_length=500 , blank=True , default='' )
    phone =  models.CharField(max_length=100 , blank=True)
    Image = models.ImageField(upload_to='service_center/', verbose_name="Image" ,default='service_center/default-image.jpg')
    Icon = models.ImageField(upload_to='service_center/Icon/', verbose_name="icon" , default='service_center/Icon/default-logo.png')
    QR = models.ImageField(upload_to='service_center/QR/', verbose_name="QR" , blank=True)
    is_online = models.BooleanField(default=False)
    isAutoAccept = models.BooleanField(default=True)
    

    def __str__(self):
        """String for representing the Model object."""
        return self.name


    def save(self, *args, **kwargs):
        scName = Service_center.objects.get(id = self.id).name
        if(scName != self.name):
            qrcode_img = qrcode.make(self.name)
            canvas = Image.new('RGB', (290, 290), 'white')
            canvas.paste(qrcode_img)
            fname = f'QR-{self.name}.png'
            buffer = BytesIO()
            canvas.save(buffer,'PNG')
            self.QR.save(fname, File(buffer), save=False)
            canvas.close()
        super(Service_center,self).save(*args, **kwargs)


@receiver(post_save, sender=Service_center)
def onService_centerCreate(sender, instance, created, **kwargs):
    if created:
        Work_time.objects.create(Service_center=instance)
        # s =  instance.id
        # url = pyqrcode.create(s)
        # url.png('media\images\service_center\QR\qr-'+ instance.name + '.png' , scale = 6)   

        # qrcode_img = qrcode.make(instance.id)
        # canvas = Image.new('RGB', (512, 512), 'white')
        # canvas.paste(qrcode_img)
        # fname = f'qr_code-{instance.name}.png'
        # buffer = BytesIO()
        # canvas.save(buffer,'PNG')
        # instance.QR=(fname, File(buffer)) 
        # instance.save()
        # canvas.close()


# @receiver(post_save, sender=Service_center)
# def onService_centerSave(sender, instance, created, **kwargs):
#     if created == False:
        # instance.Service_center.save()



class Work_time(models.Model):
    Service_center = models.OneToOneField(Service_center, on_delete=models.CASCADE)
    Saturday=models.CharField(max_length=200 , default=" no data ")
    Sunday=models.CharField(max_length=200, default=" no data ")
    Monday=models.CharField(max_length=200, default=" no data ")
    Tuesday=models.CharField(max_length=200, default=" no data ")
    Wednesday=models.CharField(max_length=200, default=" no data ")
    Thursday=models.CharField(max_length=200, default=" no data ")
    Friday=models.CharField(max_length=200, default=" no data ")
    
    
    def __str__(self):
        """String for representing the Model object."""
        return self.Monday


class Service(models.Model):
    Service_center = models.ForeignKey('Service_center', on_delete=models.CASCADE)
    name = models.CharField(max_length=350)
    IS_Active = models.BooleanField(default=True)
    time = models.IntegerField(default=0)
    
    class Meta:
        unique_together = ('Service_center', 'name',)

    
    def __str__(self):
        """String for representing the Model object."""
        return self.name 


class Service_Record(models.Model):
    Service = models.ForeignKey('Service', on_delete=models.SET_NULL, null=True)
    Employee = models.ForeignKey('Employee', on_delete=models.SET_NULL, null=True , blank=True)
    user = models.ForeignKey(User,on_delete=models.SET_NULL, null=True)
    IQ_Time = models.DateTimeField(auto_now_add=True)
    P_Time = models.DateTimeField( blank=True ,  null=True)
    O_Time = models.DateTimeField( blank=True , null=True)
    is_served = models.BooleanField(default=False)
    is_cancelled = models.BooleanField(default=False)
    status = models.CharField(
        max_length=1,
        choices= (
        ('A', 'accepted') ,
        ('P', 'pending'),
        ('R', 'rejected'),
    ),
    )

    IS_InCenter =  models.BooleanField(default=False)
    Queue_type = models.CharField(
        max_length=1,
        choices= (
        ('A', 'Has a priority') ,
        ('B', 'Has no a priority '),
    ),
        default='B',
    )
    
    version = models.IntegerField(default=0)

    def __str__(self):
        """String for representing the Model object."""
        return self.user.username

    def CallCustomer(self , emp):
        
        now = timezone.now().strftime("%Y-%m-%d %H:%M:%S.%f")

        updated = Service_Record.objects.filter(
            id = self.id,
            version=self.version,
        ).update(
            P_Time= now,
            Employee= emp ,
            version=self.version + 1,
        )

        return updated > 0

    def Customer (self , emp):
        
        now = timezone.now().strftime("%Y-%m-%d %H:%M:%S.%f")

        updated = Service_Record.objects.filter(
            id = self.id,
            version=self.version,

        ).update(
            P_Time= now,
            Employee= emp ,
            version=self.version + 1,
        )

        return updated > 0



    # def deposit(self, id, amount):
    #     updated = Account.objects.filter(
    #         id=self.id,
    #         version=self.version,
    #     ).update(
    #         balance=balance + amount,
    #         version=self.version + 1,
    #     )
    #     return updated > 0
    
    



class Black_list(models.Model):
    Service_center = models.ForeignKey('Service_center', on_delete=models.CASCADE ,null=True , blank=True )
    user = models.ForeignKey(User,on_delete=models.CASCADE )
    reason = models.CharField(max_length=600 , blank=True)
    is_BySystem = models.BooleanField(default=False)
    

    def __str__(self):
        """String for representing the Model object."""
        return self.user.username  





class White_list(models.Model):
    Service_center = models.ForeignKey('Service_center', on_delete=models.CASCADE)    
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    reason = models.CharField(max_length=600 , blank=True)

    def __str__(self):
        """String for representing the Model object."""
        return self.user.username  

class Message(models.Model):
     sender = models.CharField(max_length=700 , blank=True)
     receiver = models.IntegerField(blank=True)
     message_text = models.CharField(max_length=700 , blank=True)
     IS_read = models.BooleanField(default=False)
     
            
