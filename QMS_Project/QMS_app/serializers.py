from rest_framework import serializers

from .models import *

class Service_centerListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service_center
        fields = ['id', 'name', 'location', 'Icon']



class Work_timeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Work_time
       
        fields = ['Saturday', 'Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ['id', 'name', 'IS_Active']


class Service_center_detailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service_center
        fields = ['id', 'name', 'location', 'phone' , 'Image', 'Icon']        


