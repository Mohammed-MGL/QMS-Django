from django.shortcuts import render , redirect
from django.http import HttpResponse
from .models import Employee  , Service
from .forms import EmployeeForm , ServiceForm
from .filters import EmployeeFilter


def dashboard(request):
    context ={

    }

    return render(request ,"dashboard.html" , context) 

def employees(request):
    emps = Employee.objects.all()
    myFilter = EmployeeFilter(request.GET,queryset = emps )
    emps = myFilter.qs
    context = {
        "employees" : emps ,
        "myFilter" : myFilter,
    }
    return render(request ,"Employee/employees.html" , context) 


def addEmployee(request):

    form = EmployeeForm()

    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('employees')

    
    context ={"form":form}
    return render(request ,"Employee/employee_form.html" , context) 

def viewEmployee(request, eID):

    context = {}
    return render(request ,"Employee/employee.html" , context) 

def updateEmployee(request, eID):

    
    emp = Employee.objects.get(id = eID)
    form = EmployeeForm(instance = emp)

    if request.method == 'POST':
        form = EmployeeForm(request.POST ,instance = emp)
        if form.is_valid():
            form.save()
            return redirect('employees')

    context = {"form":form}
    return render(request ,"Employee/employee_form.html" , context) 

def deleteEmployee(request, eID):

    emp = Employee.objects.get(id = eID)
    context = {"item":emp}
    if request.method == 'POST':
        if 'Confirm' in request.POST:    
            emp.delete()
        return redirect('employees')


    return render(request ,"delete.html" , context) 



def services(request):
    service = Service.objects.all()
    context = {"serv" : service }
    return render(request ,"Service/services.html" , context) 



def addService(request):

    form = ServiceForm()

    if request.method == 'POST':
        form = ServiceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('services')

    
    context ={"form":form}
    return render(request ,"Service/service_form.html" , context) 
   


def viewService(request, sID):

    context = {}
    return render(request ,"Service/service.html" , context) 


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



def deleteService(request, sID):

    ser = Service.objects.get(id = sID)
    context = {"item":ser}

    if request.method == 'POST':
        if 'Confirm' in request.POST:    
            ser.delete()
        return redirect('services')

    return render(request ,"delete.html" , context) 

# def employeeDetails(request , eID):
#     emp = Employee.objects.get(id = eID)
#     return render(request ,"Employee.html" , {"employee" : emp}) 


# def employeeEdit(request, eID):
#     emp = Employee.objects.get(id = eID)          
#     return render(request ,"Employee.html" , {"employee" : emp}) 



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
