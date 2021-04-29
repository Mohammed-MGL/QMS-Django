from django.db import models
from django.contrib.auth.models import User , AbstractUser


class User(AbstractUser):
    is_employee = models.BooleanField(default=False)
    is_manager = models.BooleanField(default=False)
    is_guest = models.BooleanField(default=False)


class Manager(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    Service_center = models.ForeignKey('Service_center', on_delete=models.CASCADE,  null=True)

    def __str__(self):
        """String for representing the Model object."""
        return self.user.username + ' (' + self.Service_center.name+')'

class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    Service_center = models.ForeignKey('Service_center', on_delete=models.CASCADE,  null=True)
    Service = models.ForeignKey('Service', on_delete=models.SET_NULL, null=True)
    desk_num = models.CharField(max_length=50 , blank=True)
    notes =  models.CharField(max_length=1000 , blank=True)

    def __str__(self):
        """String for representing the Model object."""
        return self.user.username  

class Service_center(models.Model):
    name = models.CharField(max_length=300)
    location = models.CharField(max_length=500 , blank=True)
    # mapLocations = models.CharField(max_length=500 , blank=True)
    phone =  models.CharField(max_length=100 , blank=True, help_text='Contact phone number')
    Image = models.ImageField(upload_to='service_center/', verbose_name="Image" , blank=True)
    Icon = models.ImageField(upload_to='service_center/Icon/', verbose_name="icon" , blank=True)
    QR = models.ImageField(upload_to='service_center/QR/', verbose_name="QR" , blank=True)

    def __str__(self):
        """String for representing the Model object."""
        return self.name



class Work_time(models.Model):
    Service_center = models.OneToOneField(Service_center, on_delete=models.CASCADE)
    Saturday=models.CharField(max_length=500)
    Sunday=models.CharField(max_length=500)
    Monday=models.CharField(max_length=500)
    Tuesday=models.CharField(max_length=500)
    Wednesday=models.CharField(max_length=500)
    Thursday=models.CharField(max_length=500)
    Friday=models.CharField(max_length=500)
    
    
    def __str__(self):
        """String for representing the Model object."""
        return self.Monday


class Service(models.Model):
    Service_center = models.ForeignKey('Service_center', on_delete=models.CASCADE)
    name = models.CharField(max_length=350)
    IS_Active = models.BooleanField(default=True)
    
    
    def __str__(self):
        """String for representing the Model object."""
        return self.name 


class Service_Record(models.Model):
    Service = models.ForeignKey('Service', on_delete=models.SET_NULL, null=True)
    Employee = models.ForeignKey('Employee', on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(User,on_delete=models.SET_NULL, null=True)
    IQ_Time = models.DateTimeField(auto_now_add=True)
    P_Time = models.DateTimeField( blank=True ,  null=True)
    O_Time = models.DateTimeField( blank=True , null=True)
    is_accept = models.BooleanField(default=True)
    is_served = models.BooleanField(default=False)

    
    
    IS_InCenter =  models.BooleanField(default=False)
    Queue_type = models.CharField(
        max_length=1,
        choices= (
        ('A', 'Has a priority') ,
        ('B', 'Has no a priority '),
    ),
        default='B',
    )
    

    # def __str__(self):
    #     """String for representing the Model object."""
    #     return self.user   



class Black_list(models.Model):
    Service_center = models.ForeignKey('Service_center', on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.SET_NULL, null=True)
    

    def __str__(self):
        """String for representing the Model object."""
        return self.user   


class System_Black_list(models.Model):
    user = models.ForeignKey(User,on_delete=models.SET_NULL, null=True)
    reason = models.CharField(max_length=600 , blank=True)

    def __str__(self):
        """String for representing the Model object."""
        return self.user   


class White_list(models.Model):
    Service_center = models.ForeignKey('Service_center', on_delete=models.CASCADE)    
    user = models.ForeignKey(User,on_delete=models.SET_NULL, null=True)
    reason = models.CharField(max_length=600 , blank=True)

    def __str__(self):
        """String for representing the Model object."""
        return self.user   


# from django.db import models
# from django.contrib.auth.models import User

# # Create your models here.

# class Service_center(models.Model):
#     name = models.CharField(max_length=300 , unique= True)
#     location = models.CharField(max_length=500)
#     phone =  models.CharField(max_length=100 , blank=True, help_text='Contact phone number')
#     QR = models.ImageField(upload_to='images/service_center/QR/', verbose_name="QR" , blank=True)
#     Image = models.ImageField(upload_to='images/service_center/', verbose_name="Image" , blank=True)
#     Icon = models.ImageField(upload_to='images/service_center/Icon/', verbose_name="icon" , blank=True)
    
#     def __str__(self):
#         """String for representing the Model object."""
#         return self.name


# class Work_time(models.Model):
#     Service_center = models.OneToOneField(Service_center, on_delete=models.CASCADE)
#     Sunday=models.CharField(max_length=300)
#     Monday=models.CharField(max_length=300)
#     Tuesday=models.CharField(max_length=300)
#     Wednesday=models.CharField(max_length=300)
#     Thursday=models.CharField(max_length=300)
#     Friday=models.CharField(max_length=300)
#     Saturday=models.CharField(max_length=300)
    
#     def __str__(self):
#         """String for representing the Model object."""
#         return self.Monday


# class Service(models.Model):
#     Service_center = models.ForeignKey('Service_center', on_delete=models.CASCADE)
#     name = models.CharField(max_length=350)
#     number_of_provider = models.IntegerField()
#     time_of_provid = models.IntegerField()    

#     def __str__(self):
#         """String for representing the Model object."""
#         return self.name 


# class Service_Record(models.Model):
#     Service = models.ForeignKey('Service', on_delete=models.SET_NULL, null=True)
#     Employee = models.ForeignKey('Employee', on_delete=models.SET_NULL, null=True)
#     user = models.ForeignKey(User,on_delete=models.SET_NULL, null=True)
#     DateTime = models.DateTimeField(auto_now_add=True)
#     Accepted =  models.BooleanField(default=False)
    
#     def __str__(self):
#         """String for representing the Model object."""
#         return self.user + " " + self.Service + " " +self.Employee  + " " +self.Accepted + " " + self.DateTime


# class Employee(models.Model):   
#     name = models.CharField(max_length=300)
#     IS_MANAGER =  models.BooleanField(default=False)
#     location = models.CharField(max_length=300)
#     phone =  models.CharField(max_length=100 , blank=True, help_text='Contact phone number')
#     Service_center = models.ForeignKey('Service_center', on_delete=models.SET_NULL, null=True)

#     def __str__(self):
#         """String for representing the Model object."""
#         return self.name  


# class White_list(models.Model):
#     Service_center = models.ForeignKey('Service_center', on_delete=models.CASCADE)
#     Employee = models.ForeignKey('Employee', on_delete=models.SET_NULL, null=True)
#     user = models.ForeignKey(User,on_delete=models.SET_NULL, null=True)


# class Black_list(models.Model):
#     Service_center = models.ForeignKey('Service_center', on_delete=models.CASCADE)
#     Employee = models.ForeignKey('Employee', on_delete=models.SET_NULL, null=True)
#     user = models.ForeignKey(User,on_delete=models.SET_NULL, null=True)
        