from django.shortcuts import render , redirect
# from django.http import HttpResponse
from .models import *
from .forms import *
from .filters import EmployeeFilter , UserFilter
from django.contrib import messages
from django.contrib.auth import authenticate ,login , logout
from django.contrib.auth.decorators import login_required
from .decorators import unauthenticated_user , manager_only , employee_only

from django.contrib.auth import update_session_auth_hash
from django.utils import timezone
from datetime import timedelta, date, time, datetime 
import math
# from datetime import date
import random  
import string  
from .models import EmpMessage
from firebase_admin.messaging import Message ,Notification
from fcm_django.models import FCMDevice 

    # messages.info(request, 'info.')
    # messages.success(request, 'success')
    # messages.warning(request, 'warning.')
    # messages.error(request, 'error')



@unauthenticated_user
def loginPage(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')  
        user = authenticate(request , username = username ,password = password )

        if user is not None:
            login(request , user)
            if user.is_manager == True:
                messages.info(request, 'welcome '+username)
                return redirect('dashboard')
                
            if user.is_employee == True:
                messages.info(request, 'welcome '+ username)
                return redirect('home')
               

            if user.is_superuser == True:
                return redirect('admin:index')
            else:
                return redirect('logout')
            

        else:
            messages.warning(request, 'username and password do not match!')

    context ={}
    return render(request ,"login.html" , context) 



# @login_required(login_url='login')
def logoutUser(request):
    logout(request)
    return redirect('login')


# dashboard
@login_required(login_url='login')
@manager_only
def dashboard(request):
    sc = Manager.objects.get(user = request.user ).Service_center
    emps = Employee.objects.filter(Service_center = sc)
    
    customerAtEmp = Service_Record.objects.filter(status ='A', is_served= False, is_cancelled= False,  Employee__in=emps).count()
    service =Service.objects.filter(Service_center = sc)
    
    
    today_min = datetime.combine(timezone.now().date(), datetime.today().time().min)
    today_max = datetime.combine(timezone.now().date(), datetime.today().time().max)
    
    CustomerNumberonline = Service_Record.objects.filter(Service__in= service ,status ='A' ,is_served= False ,is_cancelled= False  ,IS_InCenter= False ,IQ_Time__range=(today_min, today_max) ).count() 
   
    # CustomerNumberonline = CustomerNumberonline.count() 

    CustomerNumberOnSConline = Service_Record.objects.filter(Service__in= service ,status ='A' ,is_served= False ,is_cancelled= False  ,IS_InCenter= True ,IQ_Time__range=(today_min, today_max)  )
   
    CustomerNumberOnSConline = CustomerNumberOnSConline.count() 

    ServiedCustomerNumberonline= Service_Record.objects.filter(Service__in= service ,is_served= True,is_cancelled= False ,P_Time__range=(today_min, today_max)).count() 
    



    class EmpDetails:
        
        name = None
        EmployeeServiedCustomerNumber = None
        service = None
        
        

        def __init__(self ,name  ,EmployeeServiedCustomerNumber , service):
            self.name = name
            
            self.EmployeeServiedCustomerNumber = EmployeeServiedCustomerNumber
            self.service = service
            

    empList = [] 
    for s in emps:
        name = s.user
        employees = Employee.objects.filter(Service_center = sc ,Service=s.Service)
        empservice = s.Service 
        

        EmployeeServiedCustomerNumber= Service_Record.objects.filter(Employee=s, status ='A' ,is_served= True,is_cancelled= False ,P_Time__range=(today_min, today_max) ).count() 
    
        ed = EmpDetails( name ,EmployeeServiedCustomerNumber , empservice  )
        
        empList.append(ed)
   




    
    class ServiceDetails:
        
        CustomerNumber = None
        CustomerNumberOnSC   = None
        ServiedCustomerNumber  = None
        name =None
        

        def __init__(self ,name,CustomerNumber ,CustomerNumberOnSC , ServiedCustomerNumber):
            self.CustomerNumber = CustomerNumber
            self.CustomerNumberOnSC = CustomerNumberOnSC
            self.ServiedCustomerNumber = ServiedCustomerNumber
            self.name = name

    sdList = [] 
    for s in service:
        name = s.name
        CustomerNumber = Service_Record.objects.filter(status ='A' ,is_served= False ,is_cancelled= False ,IS_InCenter= False,Service = s,IQ_Time__range=(today_min, today_max) ).count()
        CustomerNumberOnSC = Service_Record.objects.filter(status ='A' ,is_served= False ,is_cancelled= False  ,IS_InCenter= True   , Service = s ,IQ_Time__range=(today_min, today_max) ).count()
        
        ServiedCustomerNumber = Service_Record.objects.filter(status ='A' ,is_served= True,is_cancelled= False , Service = s ,P_Time__range=(today_min, today_max) ).count() 
        sd = ServiceDetails( name ,CustomerNumber,CustomerNumberOnSC,ServiedCustomerNumber  )
        
        sdList.append(sd)
 
    
    pendingCustomers  = Service_Record.objects.filter(Service__in= service ,is_served= False,is_cancelled= False , status ='P' ,IQ_Time__range=(today_min, today_max) ).order_by("-IQ_Time")
    acceptedCustomers = Service_Record.objects.filter(Service__in= service ,is_served= False,is_cancelled= False , status ='A' ,IQ_Time__range=(today_min, today_max) ).order_by("-IQ_Time")
    rejectedCustomers = Service_Record.objects.filter(Service__in= service ,is_served= False,is_cancelled= False , status ='R' ,IQ_Time__range=(today_min, today_max) ).order_by("-IQ_Time")
    
    context ={
        'empList':empList,
        'sc':sc,
        'ServiedCustomerNumber':ServiedCustomerNumberonline ,
        'CustomerNumber':CustomerNumberonline ,
        'CustomerNumberOnSC':CustomerNumberOnSConline ,
        'employees':emps ,
        'pendingCustomers':pendingCustomers,
        'acceptedCustomers':acceptedCustomers,
        'rejectedCustomers':rejectedCustomers,
        'customerAtEmp':customerAtEmp ,

        
        'sdList':sdList ,
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

    context = {
        'sc':sc,
        "employees" : emps ,
        "empFilter" : empFilter,
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
            messages.success(request, 'employee added ^_^')
            return redirect('employees')
    
    context ={"form":form,'sc':sc}
    return render(request ,"Employee/employeeCreationForm.html" , context) 

   
@login_required(login_url='login')
@manager_only
def viewEmployee(request, eID):
    sc = Manager.objects.get(user = request.user ).Service_center
    emp = Employee.objects.get(user = eID)
    emps = Employee.objects.filter(Service_center = sc.id)
    if not emp in emps:
        return redirect('employees')

    
    CustomerNumber= Service_Record.objects.filter(status ='A' ,is_served= False ,is_cancelled= False , IS_InCenter= True ,Employee = emp )
   
    CustomerNumber =CustomerNumber.count() 
    
    today_min = datetime.combine(timezone.now().date(), datetime.today().time().min)
    today_max = datetime.combine(timezone.now().date(), datetime.today().time().max)
    
    todayRecord = Service_Record.objects.filter(
        Employee=emp,
        is_served = True,
        P_Time__range=(today_min, today_max)        
        ).order_by('P_Time')

    totalServingTime = 0
    avrageServingTime = 0 
    customerNumberDay = 0

    if todayRecord:
        for i in todayRecord:

            servingTime  = i.O_Time - i.P_Time 
            totalServingTime += servingTime.seconds
            customerNumberDay += 1

        avrageServingTime = math.ceil(totalServingTime / todayRecord.count())

    totalServingTime = timedelta(seconds=totalServingTime)
    avrageServingTime = timedelta(seconds=avrageServingTime)



    totalServingTime_month = 0
    avrageServingTime_month = 0
    customerNumberMonth = 0
 
    
    monthRecord = Service_Record.objects.filter(
        Employee=emp,
        is_served = True,
        P_Time__month = today_min.month,
        P_Time__year = today_min.year,

        )


    if monthRecord:
        for i in monthRecord:

            servingTime  = i.O_Time - i.P_Time 
            totalServingTime_month += servingTime.seconds
            customerNumberMonth += 1

        avrageServingTime_month =math.ceil(totalServingTime_month / monthRecord.count())

    totalServingTime_month = timedelta(seconds=totalServingTime_month)

    avrageServingTime_month = timedelta(seconds=avrageServingTime_month)
    
    avrageServingTime_year =0
    totalServingTime_year=0
    yearhRecord = Service_Record.objects.filter(
        Employee=emp,
        is_served = True,
        
        P_Time__year = today_min.year,

        )
    customerNumberyear =0
    if yearhRecord:
        for i in yearhRecord:

            servingTime  = i.O_Time - i.P_Time 
            totalServingTime_year += servingTime.seconds
            customerNumberyear += 1

        avrageServingTime_year =math.ceil(totalServingTime_year / yearhRecord.count())

    totalServingTime_year = timedelta(seconds=totalServingTime_year)

    avrageServingTime_year = timedelta(seconds=avrageServingTime_year)




    
    avrageServingTime_all =0
    totalServingTime_all=0
    allRecord = Service_Record.objects.filter(
        Employee=emp,
        is_served = True,

        )
    customerNumberall =0
    if allRecord:
        for i in allRecord:

            servingTime  = i.O_Time - i.P_Time 
            totalServingTime_all += servingTime.seconds
            customerNumberall  += 1

        avrageServingTime_all =math.ceil(totalServingTime_all / allRecord.count())

    totalServingTime_all = timedelta(seconds=totalServingTime_all)

    avrageServingTime_all = timedelta(seconds=avrageServingTime_all)    
    



    ServiedCustomerNumber= Service_Record.objects.filter(status ='A' ,is_served= True,is_cancelled= False  ,Employee=emp ).count() 
        


    context = {
        'sc':sc,
        'emp':emp ,
        'CustomerNumber':CustomerNumber ,
        'totalServingTime':totalServingTime ,
        'ServiedCustomerNumber':ServiedCustomerNumber ,
        'avrageServingTime':avrageServingTime ,
        'totalServingTime_month':totalServingTime_month ,
        'avrageServingTime_month':avrageServingTime_month ,
        'totalServingTime_year':totalServingTime_year ,
        'avrageServingTime_year':avrageServingTime_year ,
        'totalServingTime_all':totalServingTime_all ,
        'avrageServingTime_all':avrageServingTime_all ,
        'customerNumberDay':customerNumberDay ,
        'customerNumberMonth':customerNumberMonth ,
        'customerNumberyear':customerNumberyear ,
        'customerNumberall':customerNumberall ,

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
            customerAtEmp = Service_Record.objects.filter( is_served= False, is_cancelled= False,  Employee=emp).count()
            if customerAtEmp>0:
                messages.error(request, 'The employee is serving a customer')
                return redirect('employees')
            form.save()
            messages.info(request, 'Employee updated')
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
            return redirect('employees')
        else:
            messages.error(request, 'Please correct the error below.')


    context = {
        "form":form,
        'sc':sc,
        'emp':emp,
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
            update_session_auth_hash(request, user)  
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
    

    
# @login_required(login_url='login')
# @manager_only
# def ManagerProfile(request):

#     user = request.user
#     sc = Manager.objects.get(user = user ).Service_center

    
#     passwordChangeForm = PasswordChangeForm(user)

#     if request.method == 'POST':
#         passwordChangeForm = PasswordChangeForm(user, request.POST)
#         if passwordChangeForm.is_valid():
#             user = passwordChangeForm.save()
#             update_session_auth_hash(request, user)  
#             messages.success(request, 'password was successfully updated!')
#             return redirect('dashboard')
#         else:
#             messages.error(request, 'Please correct the error below.')


#     context = {
#         "passwordChangeForm":passwordChangeForm,
#         'sc':sc,
#         'user':user

#         }
#     return render(request ,"ManagerProfile.html" , context) 



@login_required(login_url='login')
@manager_only
def deleteEmployee(request, eID):
     


    sc = Manager.objects.get(user = request.user ).Service_center
    emp = Employee.objects.get(user = eID)
    emps = Employee.objects.filter(Service_center = sc.id)

    if not emp in emps:
        return redirect('employees')

    if request.method == 'POST' and 'Cancel' in request.POST:
        return redirect('employees')     

    if request.method == 'POST' and 'Confirm' in request.POST:
        customerAtEmp = Service_Record.objects.filter( is_served= False, is_cancelled= False,  Employee=emp).count()
        if customerAtEmp>0:
            messages.error(request, 'The employee is serving a customer')
            return redirect('employees')

        else:

            emp.delete()
            messages.success(request, 'employee deleted')
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
def viewService(request, sID  ):
    service = Service.objects.get(id=sID)

    sc = Manager.objects.get(user = request.user ).Service_center

    services= Service.objects.filter(Service_center = sc  )

    if not service in services:
        return redirect('services')
        
    emps = Employee.objects.filter( Service = service  ) 

    today_min = datetime.combine(timezone.now().date(), datetime.today().time().min)
    today_max = datetime.combine(timezone.now().date(), datetime.today().time().max)
    
    todayRecord = Service_Record.objects.filter(
        Service=service,
        is_served = True,
        P_Time__range=(today_min, today_max)        
        ).order_by('P_Time')

    totalServingTime = 0
    avrageServingTime = 0 
    customerNumberDay = 0

    if todayRecord:
        for i in todayRecord:

            servingTime  = i.O_Time - i.P_Time 
            totalServingTime += servingTime.seconds
            customerNumberDay += 1

            

        avrageServingTime =math.ceil(totalServingTime / todayRecord.count())

    totalServingTime = timedelta(seconds=totalServingTime)
    avrageServingTime = timedelta(seconds=avrageServingTime)

    totalServingTime_month = 0
    avrageServingTime_month = 0
    customerNumberMonth = 0
 
    monthRecord = Service_Record.objects.filter(
        Service=service,
        is_served = True,
        P_Time__month = today_min.month,
        P_Time__year = today_min.year,

        )

    

    if monthRecord:
        for i in monthRecord:

            servingTime  = i.O_Time - i.P_Time 
            totalServingTime_month += servingTime.seconds
            customerNumberMonth += 1

        avrageServingTime_month =math.ceil(totalServingTime_month / monthRecord.count())

    totalServingTime_month = timedelta(seconds=totalServingTime_month)

    avrageServingTime_month = timedelta(seconds=avrageServingTime_month)
    
    avrageServingTime_year =0
    totalServingTime_year=0
    yearhRecord = Service_Record.objects.filter(
        Service=service,
        is_served = True,
        
        P_Time__year = today_min.year,

        )
    customerNumberyear =0
    if yearhRecord:
        for i in yearhRecord:

            servingTime  = i.O_Time - i.P_Time 
            totalServingTime_year += servingTime.seconds
            customerNumberyear += 1

        avrageServingTime_year =math.ceil(totalServingTime_year / yearhRecord.count())

    totalServingTime_year = timedelta(seconds=totalServingTime_year)

    avrageServingTime_year = timedelta(seconds=avrageServingTime_year)

    avrageServingTime_all =0
    totalServingTime_all=0
    allRecord = Service_Record.objects.filter(
        Service=service,
        is_served = True,

        )
    customerNumberall =0
    if allRecord:
        for i in allRecord:

            servingTime  = i.O_Time - i.P_Time 
            totalServingTime_all += servingTime.seconds
            customerNumberall  += 1

        avrageServingTime_all =math.ceil(totalServingTime_all / allRecord.count())

    totalServingTime_all = timedelta(seconds=totalServingTime_all)

    avrageServingTime_all = timedelta(seconds=avrageServingTime_all)    

    ServiedCustomerNumber= Service_Record.objects.filter(status ='A' ,is_served= True,is_cancelled= False ,Service=service ).count() 
        


    context = {
        'service' : service ,
        'sc':sc ,
        'emps':emps ,
        'totalServingTime':totalServingTime ,
        'ServiedCustomerNumber':ServiedCustomerNumber ,
        'avrageServingTime':avrageServingTime ,
        'totalServingTime_month':totalServingTime_month ,
        'avrageServingTime_month':avrageServingTime_month ,
        'totalServingTime_year':totalServingTime_year ,
        'avrageServingTime_year':avrageServingTime_year ,
        'totalServingTime_all':totalServingTime_all ,
        'avrageServingTime_all':avrageServingTime_all ,
        'customerNumberDay':customerNumberDay ,
        'customerNumberMonth':customerNumberMonth ,
        'customerNumberyear':customerNumberyear ,
        'customerNumberall':customerNumberall
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


 
@login_required(login_url='login')
@manager_only
def scChangeState(request):
   
    sc = Manager.objects.get(user = request.user ).Service_center
    service = Service.objects.filter(Service_center=sc)

    sc.is_online =  not sc.is_online
    sc.save()

    if sc.is_online == False:
        q = Service_Record.objects.filter(Service__in=service ,status ='A' ,is_served= False ,is_cancelled= False  ,IS_InCenter= False  )
        q2 = Service_Record.objects.filter(Service__in=service , status ='P' ,is_served= False ,is_cancelled= False  ,IS_InCenter= False  )
        q = q.union(q2)
        for book in q:
            book.status ='R'
            book.save()
            device = FCMDevice.objects.all().first()
    
            device.send_message(Message(
            notification=Notification(title=sc.name +" : book rejected", body="The service center has been closed",
            image="https://149351115.v2.pressablecdn.com/wp-content/uploads/2020/02/iStock-1163542789.jpg"
            )))
    return redirect('dashboard')    

    
@login_required(login_url='login')
@manager_only
def scChangeAutoAccept(request):

    sc = Manager.objects.get(user = request.user ).Service_center
    service = Service.objects.filter(Service_center=sc)
    sc.isAutoAccept =  not sc.isAutoAccept
    sc.save()
    if(sc.isAutoAccept):
        today_min = datetime.combine(timezone.now().date(), datetime.today().time().min)
        today_max = datetime.combine(timezone.now().date(), datetime.today().time().max)
        pendingCustomers  = Service_Record.objects.filter(Service__in =service ,is_served= False,is_cancelled= False , status ='P' ,IQ_Time__range=(today_min, today_max) )

        for c in pendingCustomers:
            c.status = 'A'
            c.save()

    return redirect('dashboard')    



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
def editWorkTime(request):
    
    sc = Manager.objects.get(user = request.user ).Service_center
    wT = Work_time.objects.get(Service_center = sc)
    form = WorkTimeChangeForm(instance =wT )

    if request.method == 'POST':
        form = WorkTimeChangeForm(request.POST ,instance = wT)
        if form.is_valid():
            form.save()
            return redirect('dashboard')

    context ={
        "form":form ,
        'sc':sc
    }

    return render(request ,"workTime_form.html" , context) 


@login_required(login_url='login')
@manager_only
def deleteService(request, sID):

    sc = Manager.objects.get(user = request.user ).Service_center
    ser = Service.objects.get(id = sID)
    sers = Service.objects.filter(Service_center = sc.id)

    if not ser in sers:
        return redirect('services')

    if request.method == 'POST' and 'Cancel' in request.POST:
        return redirect('services') 

    if request.method == 'POST' and 'Confirm' in request.POST: 
        CustomerNumber = Service_Record.objects.filter(status ='A' ,is_served= False ,is_cancelled= False ,Service = ser).count()
        if CustomerNumber == 0 : 
            ser.delete()
            return redirect('services')
        else :
            messages.error(request, 'you have a customer in this service')
            return redirect('services')


    context = {
        "item":ser,
        'sc':sc,
    }
    return render(request ,"delete.html" , context) 


# Black_list & White_list
@login_required(login_url='login')
@manager_only
def black_WhiteList(request):

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

    return render(request ,"black_WhiteList.html" , context)


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
      
    return redirect('black_WhiteList')



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
   
    return redirect('black_WhiteList')    




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
        
      
    return redirect('black_WhiteList')

    


@login_required(login_url='login')
@manager_only
def serachForUser(request):
    if not request.GET.get('username'):
        return redirect('black_WhiteList')
    sc = Manager.objects.get(user = request.user ).Service_center
    users = User.objects.filter(is_employee = False,is_manager= False ,is_guest= False ,is_superuser= False )
    users = User.objects.filter()
    usersFilter = UserFilter(request.GET, request=request,queryset = users )
    users = usersFilter.qs

    context = {
        'users':users ,
        "UserFilter" : usersFilter,
        'sc':sc,
        }
    return render(request ,"serachForUser.html" , context)



def deleteUserFromBL(request, uID):
    

    
    sc = Manager.objects.get(user = request.user ).Service_center

    u = Black_list.objects.get(id = uID)
    
    if request.method == 'POST' and 'Cancel' in request.POST:
        return redirect('black_WhiteList')     

    if request.method == 'POST' and 'Confirm' in request.POST:

        u.delete()
        messages.success(request, 'user deleted from black list')
        return redirect('black_WhiteList')
        
    context = {
        'sc':sc,
        "item":u

        }

    return render(request ,"delete.html" , context) 



def ServiceCnterscreen(request,sID):
    

    sc = Service_center.objects.get(id = sID)
    emps = Employee.objects.filter(Service_center = sID)
    
    today_min = datetime.combine(timezone.now().date(), datetime.today().time().min)
    today_max = datetime.combine(timezone.now().date(), datetime.today().time().max)


    
    class EmpDetails:
        desk_num = None
        eid = None
        def __init__(self,desk_num  ,eid ):
            self.desk_num = desk_num
            self.eid = eid
            

    sdList = [] 
    for s in emps:
        desk_num = s.desk_num
        customerAtEmp = Service_Record.objects.filter(status ='A', is_served= False, is_cancelled= False,  Employee=s).first()
        if(customerAtEmp is not None):
                customer=customerAtEmp.user_id
                
        else:
            
            customer= None  
        sd = EmpDetails(desk_num, customer)
        sdList.append(sd)
   
  
    context = {
        "sc":sc,
        'sdList':sdList ,

        }

    return render(request ,"ServiceCnterscreen.html" , context)     

    



def deleteUserFromWL(request, uID):

    sc = Manager.objects.get(user = request.user ).Service_center
    u = White_list.objects.get(id = uID)
    
    if request.method == 'POST' and 'Cancel' in request.POST:
        return redirect('black_WhiteList')     

    if request.method == 'POST' and 'Confirm' in request.POST:

        u.delete()
       
        messages.success(request, 'user deleted from white list')
        return redirect('black_WhiteList')

    context = {
        'sc':sc,
        "item":u
    }
    return render(request ,"delete.html" , context) 


def BookInServiceCenter(request, scID):
    
    Services = Service.objects.filter(Service_center=scID)
    serviceCenter = Service_center.objects.get(id = scID )
    
    class ServiceDetails:
        
        name = None
        CustomerNumber   = None
        WaitingTime  = None
        sid = None
        is_Active= None


        def __init__(self,name,CustomerNumber ,WaitingTime , sid , is_Active):
            self.name = name
            self.CustomerNumber = CustomerNumber
            self.WaitingTime = WaitingTime
            self.sid = sid
            self.is_Active = is_Active

    sdList = [] 
    for s in Services:
        name = s.name
        CustomerNumber = Service_Record.objects.filter(status ='A' ,is_served= False ,is_cancelled= False ,Service = s).count()
        WaitingTime = CustomerNumber * s.time
        
        sid=  s.id
        is_Active = s.IS_Active
        sd = ServiceDetails(name,CustomerNumber,WaitingTime , sid,is_Active)
        sdList.append(sd)

    context = {
        "sdList" : sdList,
        'serviceCenter':serviceCenter ,
    }
    
    return render(request ,"BookInServiceCenter.html" , context)    




def BookInService(request, sID):

    def random_string(letter_count, digit_count):  
        str1 = ''.join((random.choice(string.ascii_letters) for x in range(letter_count)))  
        str1 += ''.join((random.choice(string.digits) for x in range(digit_count)))  
    
        sam_list = list(str1) # it converts the string to list.  
        random.shuffle(sam_list) # It uses a random.shuffle() function to shuffle the string.  
        final_string = ''.join(sam_list)  
        return final_string 
    
    now = timezone.now().strftime("%Y-%m-%d %H:%M:%S.%f")
    
    with transaction.atomic():
        service =Service.objects.get(id = sID)
        serviceCenter =service.Service_center 
        guest = User.objects.create(username='Guest'+" "+now , is_guest= True)    
        gPassword = random_string(8,8)
        guest.set_password(gPassword)
        guest.save()
        book = Service_Record.objects.create(Service=service , user=guest , IS_InCenter = True ,  Queue_type = 'B'  , status ='A')
    
    return render(request ,"BookInService.html" , {'user':guest , 'serviceCenter':serviceCenter})





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
@manager_only
def SendMessageView(request , ID , MSG ):

    sender = request.user.username
    message = EmpMessage.objects.create(sender =sender , receiver= ID,message_text = MSG  )
    
    messages.success(request, 'The message was sended successfully. ')
    return redirect('dashboard')   

@login_required(login_url='login')
@manager_only
def SendMessageToCustomers(request  , MSG ):
    
    sc = Manager.objects.get(user = request.user ).Service_center
    services = Service.objects.filter(Service_center=sc)
    Customers  = Service_Record.objects.filter(Service__in=services ,is_served= False,is_cancelled= False , status__in=['A','P'] )
    for Customer in Customers:

        device = FCMDevice.objects.filter(user_id = Customer.user)
        device.send_message(Message(
            notification=Notification(title= sc.name + ": ", body=MSG)))

    return redirect('dashboard')   



@login_required(login_url='login')
@manager_only
def acceptUser(request , ID ):
    sc = Manager.objects.get(user = request.user ).Service_center 
    book = Service_Record.objects.get(id=ID)
    book.status = 'A'
    now = timezone.now().strftime("%Y-%m-%d %H:%M:%S.%f")
    book.IQ_Time = now
    book.save()
    device = FCMDevice.objects.filter(user_id =book.user.id) 
    device.send_message(Message(
        notification=Notification(title= sc.name +": Booked", body=" Your book has been accepted "
        )))
    return redirect('dashboard')    

@login_required(login_url='login')
@manager_only
def rejectUser(request , ID ):
    sc = Manager.objects.get(user = request.user ).Service_center
    book = Service_Record.objects.get(id=ID)
    book.status = 'R'
    # book.is_cancelled=True
    book.save()

    device = FCMDevice.objects.filter(user_id =book.user.id) 
    device.send_message(Message(
        notification=Notification(title=sc.name +" : Not booked", body=" Your book has been rejected "
        )))
        

    return redirect('dashboard')    





@login_required(login_url='login')
@employee_only
def home(request):
    emp = Employee.objects.get(user = request.user)
    sc = emp.Service_center
    
    service =emp.Service
    CustomerNumber = Service_Record.objects.filter(status ='A' ,is_served= False ,is_cancelled= False ,Service=service , IS_InCenter= True ,Employee = None )
   
    CustomerNumber = CustomerNumber.count() 


    form = MoveCustomerForm(sc)

    customerAtEmp = Service_Record.objects.filter( is_served= False, is_cancelled= False, Service=service,  Employee=emp).first()


    if request.method=='POST' and 'callNext' in request.POST:

        # CustomerCalling = Service_Record.objects.filter(status ='A' ,is_served= False ,is_cancelled= False ,Service=service ,IS_InCenter= True ).first()
        

        if(CustomerNumber>0 and customerAtEmp is  None):

            with transaction.atomic():
                lastCustomer = Service_Record.objects.filter(status ='A' ,is_served= True ,is_cancelled= False ,Service=service ,IS_InCenter= True,Employee=emp).order_by('O_Time').last()
                
                if(lastCustomer == None):
                    Customers = Service_Record.objects.filter(status ='A' ,is_served= False ,is_cancelled= False ,Service=service ,IS_InCenter= True, Queue_type= 'A' ,Employee = None )
                    if Customers.first() == None:
                        Customers = Service_Record.objects.filter(status ='A' ,is_served= False ,is_cancelled= False ,Service=service ,IS_InCenter= True, Queue_type= 'B',Employee = None  )
                elif(lastCustomer.Queue_type == 'B'):

                    Customers = Service_Record.objects.filter(status ='A',is_served= False ,is_cancelled= False ,Service=service ,IS_InCenter= True, Queue_type= 'A',Employee = None  )
                    if Customers.first() == None:
                        Customers = Service_Record.objects.filter(status ='A' ,is_served= False ,is_cancelled= False ,Service=service ,IS_InCenter= True, Queue_type= 'B' ,Employee = None )
                        
                else:
                    Customers = Service_Record.objects.filter(status ='A' ,is_served= False ,is_cancelled= False ,Service=service ,IS_InCenter= True, Queue_type= 'B',Employee = None  )
                
                now = timezone.now().strftime("%Y-%m-%d %H:%M:%S.%f")

                CustomerCalling = Customers.first()

                updated = Service_Record.objects.filter(
                    id = CustomerCalling.id,
                    version=CustomerCalling.version,
                ).update(
                    P_Time= now,
                    Employee= emp ,
                    version=CustomerCalling.version + 1,
                )

                device = FCMDevice.objects.filter(user_id = CustomerCalling.user.id)
                device.send_message(Message(
                notification=Notification( title=sc.name +" : It's your turn ", body="Go to deck number : "+ emp.desk_num
                )))

                if(Customers.count() > 3 ):
                    device = FCMDevice.objects.filter(user_id = Customers[3].user.id)
                    device.send_message(Message(
                    notification=Notification(title=sc.name +" : your turn is near ", body="Be ready for your turn "
                    )))

                # send
            # now = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")

            # CustomerCalling.P_Time = now
            # CustomerCalling.Employee = emp
            # CustomerCalling.save()
            # print( CustomerCalling.user)
            # CustomerCalling.CallCustomer(emp)
            # print(emp )
            # print(CustomerCalling)
            # print("...")


    elif request.method=='POST' and 'userServed' in request.POST:

        if(customerAtEmp is not None):

            customer = None  
            # CustomerCalling = Service_Record.objects.filter(status ='A' , is_served= False,is_cancelled= False ,Service=service , IS_InCenter= True,Employee=emp).first()
            now = timezone.now().strftime("%Y-%m-%d %H:%M:%S.%f")

            customerAtEmp.O_Time = now
            customerAtEmp.is_served = True 
            customerAtEmp.save()


    elif request.method == 'POST' and 'send' in request.POST:

        
        if(customerAtEmp is not None):

            form = MoveCustomerForm(sc ,data=request.POST)
            if form.is_valid():
                # CustomerCalling = Service_Record.objects.filter(status ='A',is_served= False ,is_cancelled= False ,Service=service ,IS_InCenter= True,Employee=emp).first()
                
                now = timezone.now().strftime("%Y-%m-%d %H:%M:%S.%f")

                customerAtEmp.O_Time = now
                customerAtEmp.is_served = True 
                customerAtEmp.save()

                customer = customerAtEmp.user

                ser = form.cleaned_data['Service']

                with transaction.atomic():
                    is_have_book = Service_Record.objects.filter(Service=ser , user=customer ,status ='A' , is_served= False ).first()
                    if is_have_book is not None:
                        is_have_book.is_cancelled= True
                        is_have_book.save()
                    
                    book = Service_Record.objects.create(Service=ser , user=customer , IS_InCenter = True ,  Queue_type = 'A' )

                    device = FCMDevice.objects.filter(user_id =customer.id) 
                    device.send_message(Message(
                        notification=Notification(title=sc.name +" : You have been transferred", body="A book has been registered for "+ ser.name 
                        )))
 
 
    customerAtEmp = Service_Record.objects.filter(status ='A', is_served= False, is_cancelled= False, Service=service, IS_InCenter= True, Employee=emp).first()
    if(customerAtEmp is not None):
        customer=customerAtEmp.user
        startTime= customerAtEmp.P_Time
    else:
        startTime= None
        customer= None  
    

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

        avrageServingTime = totalServingTime / todayRecord.count()


    totalServingTime = timedelta(seconds=totalServingTime)

    avrageServingTime = timedelta(seconds=avrageServingTime)
    
    


    
    ServiedCustomerNumber= Service_Record.objects.filter(status ='A' ,is_served= True,is_cancelled= False ,Service=service ,Employee=emp,P_Time__range=(today_min, today_max)         ).count() 
    CustomerNumber= Service_Record.objects.filter(status ='A' ,is_served= False ,is_cancelled= False ,Service=service ,IS_InCenter = True  ,Employee = None)
    CustomerNumber =CustomerNumber.count() 
    
    Messsagesemp = EmpMessage.objects.filter(receiver = emp.user_id , IS_read= False )
    for msg in Messsagesemp:
        messages.info(request, msg.message_text)
        msg.IS_read = True
        msg.save()
    context = {
        'sc':sc,
        'emp':emp ,
        'CustomerNumber':CustomerNumber ,
        'ServiedCustomerNumber':ServiedCustomerNumber ,
        'form': form ,
        'Customer' : customer,
        'TotalServingTime': totalServingTime ,
        'avrageServingTime':str(avrageServingTime).split('.')[0] ,
        'startTime':startTime ,

        }
    return render(request ,"EmpTemplates/home.html" , context)   

