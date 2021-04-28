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

# def OwnedbyServiceCenter(view_func):
# 	def wrapper_func(request, *args, **kwargs):

#         sc = Manager.objects.get(user = request.user ).Service_center.id
# 		if request.user.is_authenticated:
# 			return redirect('dashboard')
# 		else:
# 			return view_func(request, *args, **kwargs)

# 	return wrapper_func


def manager_only(view_func):
    def wrapper_function(request, *args, **kwargs):
        try:
            manger = Manager.objects.get(user = request.user)
            return view_func(request, *args, **kwargs)
        except Manager.DoesNotExist:
            return redirect('logout')
    return wrapper_function


# def student_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url='login'):
#     actual_decorator = user_passes_test(
#         lambda u: u.is_active and u.is_student,
#         login_url=login_url,
#         redirect_field_name=redirect_field_name
#     )
#     if function:
#         return actual_decorator(function)
#     return actual_decorator


# def teacher_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url='login'):
#     '''
#     Decorator for views that checks that the logged in user is a teacher,
#     redirects to the log-in page if necessary.
#     '''
#     actual_decorator = user_passes_test(
#         lambda u: u.is_active and u.is_teacher,
#         login_url=login_url,
#         redirect_field_name=redirect_field_name
#     )
#     if function:
#         return actual_decorator(function)
#     return actual_decorator