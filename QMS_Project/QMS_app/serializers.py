from rest_framework import serializers

from .models import *

from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password

class Service_centerListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service_center
        fields = ['id', 'name', 'location', 'Icon' ,'is_online','Image']



class Work_timeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Work_time
       
        fields = ['Saturday', 'Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']



class Qdetails(serializers.Field):

    def to_representation(self, value):

        queue = Service_Record.objects.filter(Service=value ,is_accept =True ,is_served= False ,is_cancelled= False ,Queue_type = 'B' ).count()

        ret = {
            "customersNum": queue,
            "waitingtime":"5 Min test",
            # "y": value.y_coordinate
        }
        return ret

    # def to_internal_value(self, data):
    #     ret = {
    #         "x_coordinate":' data["x"]',
    #         # "y_coordinate": data["y"],
    #     }
    #     return ret


class ServiceSerializer(serializers.ModelSerializer):

    Qdetails =Qdetails(source='*')
    # waitingTime = serializers.SerializerMethodField('is_named_bar')
    class Meta:
        model = Service
        fields = ['id', 'name', 'IS_Active','Qdetails']




class ServiceCenterNameSerializer(serializers.ModelSerializer):

    class Meta:
        model = Service_center
        fields = [ 'name' ,'Icon' ]




class ServiceNameSerializer(serializers.ModelSerializer):

    Service_center = ServiceCenterNameSerializer()
    Qdetails =Qdetails(source='*')
    class Meta:
        model = Service
        fields = [ 'id','name','Service_center' ,'Qdetails' ]


class ReservationsSerializer(serializers.ModelSerializer):

    Service = ServiceNameSerializer()
    class Meta:
        model = Service_Record
        fields = ['id','Service']



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



class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
            required=True,
            validators=[UniqueValidator(queryset=User.objects.all())]
            )

    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'password2', 'email', 'first_name', 'last_name')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )

        
        user.set_password(validated_data['password'])
        user.save()

        # refresh = RefreshToken.for_user(user)

        # return {
        #     'refresh': str(refresh),
        #     'access': str(refresh.access_token),
        # }

        return user



class ChangePasswordSerializer(serializers.ModelSerializer):
    
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    old_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('old_password', 'password', 'password2')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def validate_old_password(self, value):

        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError({"old_password": "Old password is not correct"})
        return value

    def update(self, instance, validated_data):
        user = self.context['request'].user

        if user.pk != instance.pk:
            raise serializers.ValidationError({"authorize": "You dont have permission for this user."})


        instance.set_password(validated_data['password'])
        instance.save()

        return instance        



class UpdateUserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True},
        }

    def validate_email(self, value):
        user = self.context['request'].user
        if User.objects.exclude(pk=user.pk).filter(email=value).exists():
            raise serializers.ValidationError({"email": "This email is already in use."})
        return value

    def validate_username(self, value):
        user = self.context['request'].user
        if User.objects.exclude(pk=user.pk).filter(username=value).exists():
            raise serializers.ValidationError({"username": "This username is already in use."})
        return value
        

    def update(self, instance, validated_data):
        user = self.context['request'].user

        if user.pk != instance.pk:
            raise serializers.ValidationError({"authorize": "You dont have permission for this user."})

        instance.first_name = validated_data['first_name']
        instance.last_name = validated_data['last_name']
        instance.email = validated_data['email']
        instance.username = validated_data['username']

        instance.save()

        return instance        

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name','last_name' , 'email']        



class HServiceNameSerializer(serializers.ModelSerializer):

    Service_center = ServiceCenterNameSerializer()
    
    class Meta:
        model = Service
        fields = [ 'id','name','Service_center'  ]



class HistorySerializer(serializers.ModelSerializer):
    Service = HServiceNameSerializer()
  
    status = serializers.SerializerMethodField() # add field

    

     
    class Meta:
        model = Service_Record
        fields = [ 'id' , 'Service', 'IQ_Time'  ,'status' ]  

    def get_status(self, obj):
        # here write the logic to compute the value based on object
        if obj.is_cancelled:
            return 'cancelled'

        if obj.is_served:
            return 'served'



        if  obj.is_accept == False:
            return 'not accept'    
            





            

       



     

