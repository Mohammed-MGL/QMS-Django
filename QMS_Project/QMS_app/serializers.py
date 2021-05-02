from rest_framework import serializers

from .models import *

class Service_centerListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service_center
        fields = ['id', 'name', 'location', 'Icon' ,'is_online','Image']



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
        fields = ['id', 'name', 'location', 'phone' , 'Image', 'Icon' , 'is_online', 'mapLocations']        


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user        


