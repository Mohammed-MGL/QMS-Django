from django.contrib import admin

from .models import *

# Register your models here.
admin.site.register(User)
admin.site.register(Manager)
admin.site.register(Service_center)
admin.site.register(Work_time)
admin.site.register(Employee)
admin.site.register(Service)
admin.site.register(Service_Record)
admin.site.register(White_list)
admin.site.register(Black_list)


