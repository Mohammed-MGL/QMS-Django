from django.shortcuts import render , redirect
# from django.http import HttpResponse
from .models import *
from .forms import *
from .filters import EmployeeFilter , UserFilter
from django.contrib import messages
from django.contrib.auth import authenticate ,login , logout
from django.contrib.auth.decorators import login_required
from .decorators import unauthenticated_user , manager_only , employee_only
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.utils import timezone
from datetime import timedelta, date, time, datetime 
# from datetime import date
import random  
import string  



@unauthenticated_user
def loginPage(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')  
        user = authenticate(request , username = username ,password = password )

        if user is not None:
            login(request , user)
            if user.is_manager == True:

                return redirect('dashboard')
            if user.is_employee == True:
                return redirect('home')

            
        else:
            messages.warning(request, 'username and password do not match!')

    context ={}
    return render(request ,"login.html" , context) 


@login_required(login_url='login')
def logoutUser(request):
    logout(request)
    return redirect('login')


# dashboard
@login_required(login_url='login')
@manager_only
def dashboard(request):
    sc = Manager.objects.get(user = request.user ).Service_center
    
    context ={
        'sc':sc,
    }
    return render(request ,"dashboard.html" , context) 

# employees
@login_required(login_url='login')
@manager_only
def employees(request):
    sc = Manager.objects.get(user = request.user).Service_center
    emps = Employee.objects.filter(Service_center = sc)
    empFilter = EmployeeFilter(request.GET, request=request,queryset = emps )
    emps = empFilter.qs
    # uNameFilter = UserFilter(request.GET,queryset = emps)
    # emps = uNameFilter.qs

    context = {
        'sc':sc,
        "employees" : emps ,
        "empFilter" : empFilter,
        # "uNameFilter" : uNameFilter
    }
    return render(request ,"Employee/employees.html" , context) 


@login_required(login_url='login')
@manager_only
def addEmployee(request):
    sc = Manager.objects.get(user = request.user ).Service_center
    form = EmployeeCreationForm(sc)
    if request.method == 'POST':
        form = EmployeeCreationForm(sc,data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('employees')
    
    context ={"form":form,'sc':sc}
    return render(request ,"Employee/employeeCreationForm.html" , context) 

   
@login_required(login_url='login')
@manager_only
def viewEmployee(request, eID):
    sc = Manager.objects.get(user = request.user ).Service_center
    emp = Employee.objects.get(user = eID)
    emps = Employee.objects.filter(Service_center = sc.id)

    service =emp.Service
    CustomerNumber= Service_Record.objects.filter(is_accept = True ,is_served= False ,is_cancelled= False ,Service=service , IS_InCenter= True ,Employee = None )
   
    CustomerNumber =CustomerNumber.count() 

    if not emp in emps:
        return redirect('employees')

    
    today_min = datetime.combine(timezone.now().date(), datetime.today().time().min)
    today_max = datetime.combine(timezone.now().date(), datetime.today().time().max)
    
    todayRecord = Service_Record.objects.filter(
        Employee=emp,
        is_served = True,
        P_Time__range=(today_min, today_max)        
        ).order_by('P_Time')

    totalServingTime = 0
    avrageServingTime = 0 

    if todayRecord:
        for i in todayRecord:

            servingTime  = i.O_Time - i.P_Time 
            totalServingTime += servingTime.seconds

        avrageServingTime =totalServingTime / todayRecord.count()

    totalServingTime = timedelta(seconds=totalServingTime)
    avrageServingTime = timedelta(seconds=avrageServingTime)


    ServiedCustomerNumber= Service_Record.objects.filter(is_accept = True ,is_served= True,is_cancelled= False ,Service=service ,Employee=emp ).count() 
        


    context = {
        'sc':sc,
        'emp':emp ,
        'CustomerNumber':CustomerNumber ,
        'totalServingTime':totalServingTime ,
        'ServiedCustomerNumber':ServiedCustomerNumber ,
        'avrageServingTime':avrageServingTime
        }
    return render(request ,"Employee/employee.html" , context)


@login_required(login_url='login')
@manager_only
def updateEmployee(request, eID):
    sc = Manager.objects.get(user = request.user ).Service_center
    emp = Employee.objects.get(user = eID)
    emps = Employee.objects.filter(Service_center = sc.id)

    if not emp in emps:
        return redirect('employees')

    
    form = EmployeeForm(sc,instance = emp)

    if request.method == 'POST':
        form = EmployeeForm(sc,request.POST ,instance = emp)
        if form.is_valid():
            form.save()
            return redirect('employees')

    context = {
        "form":form,
        'sc':sc,
         'eID':eID
        }
    return render(request ,"Employee/employeeUpdate.html" , context) 


@login_required(login_url='login')
@manager_only
def updateEmployeePassWord(request, eID):
    sc = Manager.objects.get(user = request.user ).Service_center
    emp = Employee.objects.get(user = eID)
    emps = Employee.objects.filter(Service_center = sc.id)

    if not emp in emps:
        return redirect('employees')

    form = PasswordChangeForm(emp.user)

    if request.method == 'POST':
        form = PasswordChangeForm(emp.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'password was successfully updated!')
            # messages.success(request, 'Your password was successfully updated!')
            return redirect('employees')
        else:
            messages.error(request, 'Please correct the error below.')

   

    context = {
        "form":form,
        'sc':sc,
        }
    return render(request ,"Employee/employeePassWordUpdate.html" , context) 


@login_required(login_url='login')
@manager_only
def ManagerProfile(request):

    user = request.user
    sc = Manager.objects.get(user = user ).Service_center

    
    passwordChangeForm = PasswordChangeForm(user)

    if request.method == 'POST':
        passwordChangeForm = PasswordChangeForm(user, request.POST)
        if passwordChangeForm.is_valid():
            user = passwordChangeForm.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'password was successfully updated!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Please correct the error below.')


    context = {
        "passwordChangeForm":passwordChangeForm,
        'sc':sc,
        'user':user

        }
    return render(request ,"ManagerProfile.html" , context) 



@login_required(login_url='login')
@manager_only
def deleteEmployee(request, eID):

    sc = Manager.objects.get(user = request.user ).Service_center
    emp = Employee.objects.get(user = eID)
    emps = Employee.objects.filter(Service_center = sc.id)

    if not emp in emps:
        return redirect('employees')

    if request.method == 'POST':
        if 'Confirm' in request.POST:    
            emp.delete()
        return redirect('employees')

    context = {
        'item':emp,
        'sc':sc,
    }
    return render(request ,"delete.html" , context) 


# services
@login_required(login_url='login')
@manager_only
def services(request):
    
    sc = Manager.objects.get(user = request.user ).Service_center
    service = Service.objects.filter(Service_center=sc)

    form = ServiceForm(sc)

    if request.method == 'POST':
        form = ServiceForm(sc,request.POST)
        if form.is_valid():
            form.save()
            return redirect('services')

    context = {
        "serv" : service,
        "form":form,
        'sc':sc,

    }
    return render(request ,"Service/services.html" , context) 



@login_required(login_url='login')
@manager_only
def viewService(request, sID):
    service = Service.objects.get(id=sID)

    sc = Manager.objects.get(user = request.user ).Service_center

    services= Service.objects.filter(Service_center = sc )

    if not service in services:
        return redirect('services')

    context = {
        'service' : service ,
        'sc':sc
    }
    return render(request ,"Service/service.html" , context) 



 
@login_required(login_url='login')
@manager_only
def serviceChangeState(request, sID):
    service = Service.objects.get(id=sID)

    sc = Manager.objects.get(user = request.user ).Service_center

    services= Service.objects.filter(Service_center = sc )

    if not service in services:
        return redirect('services')
   
    service.IS_Active =  not service.IS_Active
    service.save()
    return redirect('services')


# @login_required(login_url='login')
# @manager_only
# def serviceCenterChangeState(request):
    

#     sc = Manager.objects.get(user = request.user ).Service_center
#     context = {
#         'sc' : sc
#     }
#     return render(request ,"base_generic.html" , context) 

     
   

#koko
    # context = {
    #     'service' : service
    # }
    # return render(request ,"Service/service.html" , context)    

@login_required(login_url='login')
@manager_only
def editService(request, sID):

    
    sc = Manager.objects.get(user = request.user ).Service_center
    ser = Service.objects.get(id = sID)
    form = ServiceForm(sc,instance = ser)

    if request.method == 'POST':
        form = ServiceForm(sc ,request.POST ,instance = ser)
        if form.is_valid():
            form.save()
            return redirect('services')

    context ={
        "form":form ,
        'sc':sc
    }

    return render(request ,"Service/service_form.html" , context)     


@login_required(login_url='login')
@manager_only
def deleteService(request, sID):

    ser = Service.objects.get(id = sID)
    context = {"item":ser}

    if request.method == 'POST':
        if 'Confirm' in request.POST:    
            ser.delete()
        return redirect('services')

    return render(request ,"delete.html" , context) 


# Black_list & White_list
@login_required(login_url='login')
@manager_only
def bwlist(request):
    sc = Manager.objects.get(user = request.user ).Service_center

    w_list = White_list.objects.filter(Service_center = sc)
    b_list = Black_list.objects.filter(Service_center = sc)
    users = User.objects.filter(is_employee = False,is_manager= False ,is_guest= False ,is_superuser= False )
    usersFilter = UserFilter(request.GET, request=request,queryset = users )
    users = usersFilter.qs
    
    # if request.method == 'POST':
    #     searchWord = request.POST.get('Search')
   
    context = {
        'w_list':w_list ,
        'b_list':b_list ,
        'users':users ,
        "UserFilter" : usersFilter,
        
        'sc':sc,

        }

    return render(request ,"bwlist.html" , context)


    # addToBlackLIst

@login_required(login_url='login')
@manager_only
def addToBlackLIst(request, uID):
    sc = Manager.objects.get(user = request.user ).Service_center

    u = User.objects.get(id= uID)

    t = Black_list.objects.filter(user=u ,Service_center=sc).count()
    x = White_list.objects.filter(user=u ,Service_center=sc).count()
    if t>0:

        messages.warning(request, u.username +' already in blacklist') 

    elif  x>0:
        messages.warning(request,u.username +' already in whitelist') 

    elif  t==0 and x==0:

        Black_list.objects.create(user=u ,Service_center=sc)
      
    return redirect('bwlist')



@login_required(login_url='login')
@manager_only
def addToWhiteLIst(request, uID):
    sc = Manager.objects.get(user = request.user ).Service_center

    u = User.objects.get(id= uID)

    t = White_list.objects.filter(user=u ,Service_center=sc).count()
    x = Black_list.objects.filter(user=u ,Service_center=sc).count()

    if t>0:
        messages.warning(request, u.username +' already in whitelist') 

    elif  x>0:
        messages.warning(request,u.username +' already in Blacklist') 

    elif  t==0 and x==0:
        White_list.objects.create(user=u ,Service_center=sc)
   
    return redirect('bwlist')    




@login_required(login_url='login')
@manager_only
def systemBlackList(request):
    sc = Manager.objects.get(user = request.user ).Service_center

    SystemBlackList = Black_list.objects.filter(is_BySystem= True)
    
   
    context = {
        'SystemBlackList':SystemBlackList ,
        
        
        'sc':sc,

        }

    return render(request ,"systemBlackList.html" , context)  

    

@login_required(login_url='login')
@manager_only
def copysystemBlackList(request):
    sc = Manager.objects.get(user = request.user ).Service_center
    

    SystemBlackList = Black_list.objects.filter(is_BySystem = True)

    for bl in SystemBlackList:
        u = bl.user
        t = Black_list.objects.filter(user=u ,Service_center=sc).count()
        x = White_list.objects.filter(user=u ,Service_center=sc).count()
        if t>0:

            messages.warning(request, u.username +' already in blacklist') 

        elif  x>0:
            messages.warning(request,u.username +' already in whitelist') 

        elif  t==0 and x==0:

            Black_list.objects.create(user=u ,Service_center=sc)
        
      
    return redirect('bwlist')

    


@login_required(login_url='login')
@manager_only
def serachForUser(request):
    sc = Manager.objects.get(user = request.user ).Service_center
    users = User.objects.filter(is_employee = False,is_manager= False ,is_guest= False ,is_superuser= False )
    
    usersFilter = UserFilter(request.GET, request=request,queryset = users )
    users = usersFilter.qs
    context = {
              'users':users ,
              'sc':sc,
        }
    return render(request ,"serachForUser.html" , context)



def deleteUserFromBL(request, uID):
    sc = Manager.objects.get(user = request.user ).Service_center

    u = Black_list.objects.get(id = uID)
    context = {"item":u}
    if request.method == 'POST':
        u.delete()
        return redirect('bwlist')
    context = {
             
              'sc':sc,
        }

    return render(request ,"delete.html" , context) 



def deleteUserFromWL(request, uID):

    u = White_list.objects.get(id = uID)
    context = {"item":u}
    if request.method == 'POST':
        u.delete()
        return redirect('bwlist')

    return render(request ,"delete.html" , context) 


def BookAsGuest(request, scID):
    
    Services = Service.objects.filter(Service_center=scID)
    serviceCenter = Service_center.objects.get(id = scID )
    
    class ServiceDetails:
        
        name = None
        CustomerNumber   = None
        WaitingTime  = None
        sid = None
        def __init__(self,name,CustomerNumber ,WaitingTime , sid):
            self.name = name
            self.CustomerNumber = CustomerNumber
            self.WaitingTime = WaitingTime
            self.sid = sid

    sdList = [] 
    for s in Services:
        name = s.name
        CustomerNumber = Service_Record.objects.filter(is_accept = True ,is_served= False ,is_cancelled= False ,Service= s).count()
        WaitingTime = "5 min test"
        sid=  s.id
        sd = ServiceDetails(name,CustomerNumber,WaitingTime , sid)
        
        sdList.append(sd)


    context = {
        "sdList" : sdList,
        'serviceCenter':serviceCenter ,
    }
    
    return render(request ,"BookAsGuest.html" , context)    





def book_in_service(request, sID):
    
    now = timezone.localtime().strftime("%Y-%m-%d %H:%M:%S.%f")
    
    service =Service.objects.get(id = sID)
    serviceCenter =service.Service_center 
    guest = User.objects.create(username='Guest'+" "+now , is_guest= True)
    
    def random_string(letter_count, digit_count):  
        str1 = ''.join((random.choice(string.ascii_letters) for x in range(letter_count)))  
        str1 += ''.join((random.choice(string.digits) for x in range(digit_count)))  
    
        sam_list = list(str1) # it converts the string to list.  
        random.shuffle(sam_list) # It uses a random.shuffle() function to shuffle the string.  
        final_string = ''.join(sam_list)  
        return final_string 
    
    gPassword = random_string(8,8)
    guest.set_password(gPassword)
    guest.save()
    book = Service_Record.objects.create(Service=service , user=guest , IS_InCenter = True ,  Queue_type = 'B' )
    
    return render(request ,"book_in_service.html" , {'user':guest , 'serviceCenter':serviceCenter})





@login_required(login_url='login')
@manager_only
def ServiceCnterProfile(request):
    sc = Manager.objects.get(user = request.user ).Service_center
    
    form = scform(instance = sc)

    if request.method == 'POST':
        form = scform(data=request.POST,files=request.FILES,instance = sc)
        if form.is_valid():
            
            form.save()
            return redirect('dashboard')

    context = {
        "form":form,
        'sc':sc,
         
        }
    return render(request ,"ServiceCnterProfile.html" , context) 





@login_required(login_url='login')
@employee_only
def home(request):
    emp = Employee.objects.get(user = request.user)
    sc = emp.Service_center
    
    service =emp.Service
    CustomerNumber= Service_Record.objects.filter(is_accept = True ,is_served= False ,is_cancelled= False ,Service=service , IS_InCenter= True ,Employee = None )
   
    CustomerNumber =CustomerNumber.count() 
    

    

    form = MoveCustomerForm(sc)

    customerAtEmp = Service_Record.objects.filter(is_accept = True, is_served= False, is_cancelled= False, Service=service, IS_InCenter= True, Employee=emp).first()


    if request.method=='POST' and 'callNext' in request.POST:

        # CustomerCalling = Service_Record.objects.filter(is_accept = True ,is_served= False ,is_cancelled= False ,Service=service ,IS_InCenter= True ).first()
        

        if(CustomerNumber>0 and customerAtEmp is  None):

            lastCustomer = Service_Record.objects.filter(is_accept = True ,is_served= True ,is_cancelled= False ,Service=service ,IS_InCenter= True,Employee=emp).order_by('O_Time').last()
           
            if(lastCustomer == None):
                CustomerCalling = Service_Record.objects.filter(is_accept = True ,is_served= False ,is_cancelled= False ,Service=service ,IS_InCenter= True, Queue_type= 'A' ,Employee = None ).first()
                if CustomerCalling == None:
                    CustomerCalling = Service_Record.objects.filter(is_accept = True ,is_served= False ,is_cancelled= False ,Service=service ,IS_InCenter= True, Queue_type= 'B',Employee = None  ).first()
            elif(lastCustomer.Queue_type == 'B'):

                CustomerCalling = Service_Record.objects.filter(is_accept = True ,is_served= False ,is_cancelled= False ,Service=service ,IS_InCenter= True, Queue_type= 'A',Employee = None  ).first()
                if CustomerCalling == None:
                    
                    CustomerCalling = Service_Record.objects.filter(is_accept = True ,is_served= False ,is_cancelled= False ,Service=service ,IS_InCenter= True, Queue_type= 'B' ,Employee = None ).first()
            else:
                CustomerCalling = Service_Record.objects.filter(is_accept = True ,is_served= False ,is_cancelled= False ,Service=service ,IS_InCenter= True, Queue_type= 'B',Employee = None  ).first()
            
            # now = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")

            # CustomerCalling.P_Time = now
            # CustomerCalling.Employee = emp
            # CustomerCalling.save()
            # print( CustomerCalling.user)
            CustomerCalling.CallCustomer(emp)
            # print(emp )
            # print(CustomerCalling)
            # print("...")


    elif request.method=='POST' and 'userServed' in request.POST:

        if(customerAtEmp is not None):

            customer= None  
            CustomerCalling = Service_Record.objects.filter(is_accept = True , is_served= False,is_cancelled= False ,Service=service , IS_InCenter= True,Employee=emp).first()

            now = timezone.localtime().strftime("%Y-%m-%d %H:%M:%S.%f")

            CustomerCalling.O_Time = now
            CustomerCalling.is_served = True 
            CustomerCalling.save()


    elif request.method == 'POST' and 'send' in request.POST:

        
        if(customerAtEmp is not None):

            form = MoveCustomerForm(sc ,data=request.POST)
            if form.is_valid():
                CustomerCalling = Service_Record.objects.filter(is_accept = True,is_served= False ,is_cancelled= False ,Service=service ,IS_InCenter= True,Employee=emp).first()
                
                now = timezone.now().strftime("%Y-%m-%d %H:%M:%S.%f")

                CustomerCalling.O_Time = now
                CustomerCalling.is_served = True 
                CustomerCalling.save()

                customer = CustomerCalling.user

                ser = form.cleaned_data['Service']

                is_have_book = Service_Record.objects.filter(Service=ser , user=customer ,is_accept = True , is_served= False ).first()
                if is_have_book is not None:
                    is_have_book.is_cancelled= True
                    is_have_book.save()
                    
                book = Service_Record.objects.create(Service=ser , user=customer , IS_InCenter = True ,  Queue_type = 'A' )
    
    customerAtEmp = Service_Record.objects.filter(is_accept = True, is_served= False, is_cancelled= False, Service=service, IS_InCenter= True, Employee=emp).first()
    if(customerAtEmp is not None):
        customer=customerAtEmp.user
    else:
        customer= None  
    

    today_min = datetime.combine(timezone.now().date(), datetime.today().time().min)
    today_max = datetime.combine(timezone.now().date(), datetime.today().time().max)
    
    todayRecord = Service_Record.objects.filter(
        Employee=emp,
        is_served = True,
        P_Time__range=(today_min, today_max)        
        ).order_by('P_Time')

    totalServingTime = 0
    avrageServingTime =0 

    if todayRecord:
        for i in todayRecord:

            servingTime  = i.O_Time - i.P_Time 
            totalServingTime += servingTime.seconds

        avrageServingTime =totalServingTime / todayRecord.count()

    totalServingTime = timedelta(seconds=totalServingTime)

    avrageServingTime = timedelta(seconds=avrageServingTime)

    
    ServiedCustomerNumber= Service_Record.objects.filter(is_accept = True ,is_served= True,is_cancelled= False ,Service=service ,Employee=emp ).count() 
    CustomerNumber= Service_Record.objects.filter(is_accept = True ,is_served= False ,is_cancelled= False ,Service=service ,IS_InCenter = True  ,Employee = None)
    CustomerNumber =CustomerNumber.count() 
    context = {
        'sc':sc,
        'emp':emp ,
        'CustomerNumber':CustomerNumber ,
        'ServiedCustomerNumber':ServiedCustomerNumber ,
        'form': form ,
        'Customer' : customer,
        'TotalServingTime': totalServingTime ,
        'avrageServingTime':avrageServingTime
        }
    return render(request ,"EmployeeTemp/home.html" , context)   

