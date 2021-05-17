from django.http import HttpResponse
from django.shortcuts import redirect
from .models import *


def unauthenticated_user(view_func):
	def wrapper_func(request, *args, **kwargs):
		if request.user.is_authenticated:
			return redirect('dashboard')
		else:
			return view_func(request, *args, **kwargs)

	return wrapper_func


def manager_only(view_func):
    def wrapper_function(request, *args, **kwargs):
        try:
            manger = Manager.objects.get(user = request.user)
            return view_func(request, *args, **kwargs)
        except Manager.DoesNotExist:
            return redirect('logout')
    return wrapper_function


def employee_only(view_func):
    def wrapper_function(request, *args, **kwargs):
        try:
            employee = Employee.objects.get(user = request.user)
            return view_func(request, *args, **kwargs)
        except Employee.DoesNotExist:
            return redirect('logout')
    return wrapper_function
