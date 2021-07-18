from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import *

# Register your models here.


class CustomUserAdmin(UserAdmin):
    add_form = UserCreationForm
    form = UserChangeForm
    model = User
    list_filter = ('is_manager', 'is_employee','is_guest')
    list_display = ['id', 'email', 'username', 'first_name', 'last_name' ,'is_manager','is_employee','is_guest',]
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('email', 'first_name', 'last_name','is_superuser','is_manager' ,'is_employee','is_guest',)}),
    )
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('is_manager' ,'is_employee','is_guest',)}),
    )

admin.site.register(User, CustomUserAdmin)
admin.site.register(Manager)
admin.site.register(Service_center)
admin.site.register(Work_time)
admin.site.register(Employee)
admin.site.register(Service)
admin.site.register(Service_Record)
admin.site.register(White_list)
admin.site.register(Black_list)
admin.site.register(Message)


