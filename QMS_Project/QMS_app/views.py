from django.shortcuts import render , redirect
from django.http import HttpResponse
from .models import Employee 
from .forms import EmployeeForm


def employees(request):
    emps = Employee.objects.all()
    return render(request ,"Employee.html" , {"employees" : emps}) 


def createEmployee(request):

    form = EmployeeForm()

    if request.method == 'POST':
        print(request.POST)
        form = EmployeeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('employees')

    context ={"form":form}
    return render(request ,"employee_form.html" , context) 

def updateEmployee(request, eID):

    
    emp = Employee.objects.get(id = eID)
    form = EmployeeForm(instance = emp)

    if request.method == 'POST':
        print(request.POST)
        form = EmployeeForm(request.POST ,instance = emp)
        if form.is_valid():
            form.save()
            return redirect('employees')

    context = {"form":form}
    return render(request ,"employee_form.html" , context) 

def deleteEmployee(request, eID):

    emp = Employee.objects.get(id = eID)
    context = {"item":emp}
    if request.method == 'POST':
        emp.delete()
        return redirect('employees')


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



# def service(request):
#     return render(request ,"services.html" , {})   


# def d(request):
#     return render(request ,"dash.html" , {})   







# def addservice(request):
#     return render(request ,"addservice.html" , {})     
