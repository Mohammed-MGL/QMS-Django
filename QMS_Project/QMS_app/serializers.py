from rest_framework import serializers

from .models import *

class Service_centerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service_center
        fields = '__all__'


class Work_timeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Work_time
        fields = '__all__'


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = '__all__'

