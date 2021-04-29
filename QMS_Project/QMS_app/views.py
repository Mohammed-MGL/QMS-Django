from django.shortcuts import render , redirect
from django.http import HttpResponse
from .models import *
from .forms import *
from .filters import EmployeeFilter , UserFilter
from django.contrib import messages
from django.contrib.auth import authenticate ,login , logout
from django.contrib.auth.decorators import login_required
from .decorators import unauthenticated_user , manager_only
from django.contrib.auth.forms import PasswordChangeForm
from datetime import datetime
from datetime import date
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
            return redirect('employees')
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
        'scName':sc,
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
        'scName':sc,
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
    
    context ={"form":form,'scName':sc}
    return render(request ,"Employee/employeeCreationForm.html" , context) 

   
@login_required(login_url='login')
@manager_only
def viewEmployee(request, eID):
    sc = Manager.objects.get(user = request.user ).Service_center
    emp = Employee.objects.get(user = eID)
    emps = Employee.objects.filter(Service_center = sc.id)

    if not emp in emps:
        return redirect('employees')


    context = {
        'scName':sc,
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
        'scName':sc,
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

    form = PasswordChangeForm(request.user)

    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('employees')
        else:
            messages.error(request, 'Please correct the error below.')

    # form = EmployeeForm(instance = emp)

    # if request.method == 'POST':
    #     form = EmployeeForm(request.POST ,instance = emp)
    #     if form.is_valid():
    #         form.save()
    #         return redirect('employees')

    context = {
        "form":form,
        'scName':sc,
        }
    return render(request ,"Employee/employeePassWordUpdate.html" , context) 


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
        'scName':sc,
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
        'scName':sc,

    }
    return render(request ,"Service/services.html" , context) 


@login_required(login_url='login')
@manager_only
def addService(request):
    
    sc = Manager.objects.get(user = request.user ).Service_center

    form = ServiceForm(sc)

    if request.method == 'POST':
        form = ServiceForm(sc,request.POST)
        if form.is_valid():
            form.save()
            return redirect('services')

    
    context ={"form":form}
    return render(request ,"Service/service_form.html" , context) 
   

@login_required(login_url='login')
@manager_only
def viewService(request, sID):
    service = Service.objects.get(id=sID)

    sc = Manager.objects.get(user = request.user ).Service_center

    services= Service.objects.filter(Service_center = sc )

    if not service in services:
        return redirect('services')

    context = {
        'service' : service
    }
    return render(request ,"Service/service.html" , context) 



 
@login_required(login_url='login')
@manager_only
def serviceChangeState(request, sID):
    service = Service.objects.get(id=sID)

    sc = Manager.objects.get(user = request.user ).Service_center

    services= Service.objects.filter(Service_center = sc )

    if not service in services:
        return redirect('bwlist')
   
    service.IS_Active =  not service.IS_Active
    service.save()
    return redirect('services')
   


    # context = {
    #     'service' : service
    # }
    # return render(request ,"Service/service.html" , context)    

@login_required(login_url='login')
@manager_only
def editService(request, sID):

    
    ser = Service.objects.get(id = sID)
    form = ServiceForm(instance = ser)

    if request.method == 'POST':
        form = ServiceForm(request.POST ,instance = ser)
        if form.is_valid():
            form.save()
            return redirect('services')

    context = {"form":form}
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
   
    context = {
        'w_list':w_list ,
        'b_list':b_list ,        
        }

    return render(request ,"bwlist.html" , context)




def deleteUserFromBL(request, uID):

    u = Black_list.objects.get(id = uID)
    context = {"item":u}
    if request.method == 'POST':
        u.delete()
        return redirect('bwlist')

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

    # guest = User.objects.create()
    
    

    context = {
        "Services" : Services,
    }
    
    return render(request ,"BookAsGuest.html" , context)    





def book_in_service(request, sID):
    now = datetime.now()
    service =Service.objects.get(id = sID)
    guest = User.objects.create(username='Guest'+" "+now.strftime("%d/%m/%Y %H:%M:%S"))

    def random_string(letter_count, digit_count):  
        str1 = ''.join((random.choice(string.ascii_letters) for x in range(letter_count)))  
        str1 += ''.join((random.choice(string.digits) for x in range(digit_count)))  
    
        sam_list = list(str1) # it converts the string to list.  
        random.shuffle(sam_list) # It uses a random.shuffle() function to shuffle the string.  
        final_string = ''.join(sam_list)  
        return final_string 
    
    gPassword = random_string(8,8)
    print(gPassword)
    guest.set_password(gPassword)
    guest.save()
    book = Service_Record.objects.create(Service=service , user=guest , IS_InCenter = True ,  Queue_type = 'B' )
    
    return render(request ,"book_in_service.html" , {})

###########################################
# from django.shortcuts import render
# from django.http import HttpResponse
# from .models import User , Service_center , Employee , Black_list , White_list




# def bwlist(request):
#     ph_list = Black_list.objects.all()
    
#     context = {
#         'ph_list':ph_list }
#     return render(request ,"bwlist.html" , context)


# def dash(request):
#     return render(request ,"dashboard.html" , {})    




# def d(request):
#     return render(request ,"dash.html" , {})   







# def addservice(request):
#     return render(request ,"addservice.html" , {})     
