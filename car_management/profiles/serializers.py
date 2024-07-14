from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import User
from cars.models import Car
from trips.models import Trip
from django.shortcuts import get_object_or_404
from cars.serializers import CarSerializer

class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'role']  # Add role field

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            role=validated_data['role']  # Set the role
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')
        role = data.get('role')

        if username and password:
            user = authenticate(username=username, password=password)
            if user:
                return user
            else:
                raise serializers.ValidationError("Invalid credentials")
        else:
            raise serializers.ValidationError("Must include 'username' and 'password'")


class CarSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Car
        fields = ['car_id', 'owner', 'car_id', 'model', 'license_plate', 'available']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'address', 'phone_number']

'''
class TripSerializer(serializers.ModelSerializer):
    driver = serializers.ReadOnlyField(source='driver.username')
    car = CarSerializer(read_only=True)

    class Meta:
        model = Trip
        fields = [
            'trip_id', 
            'driver', 
            'car', 
            'status', 
            'pick_up_time', 
            'pick_up_location', 
            'drop_off_time', 
            'drop_off_location', 
            'pick_up_photos', 
            'fuel_details', 
            'trip_details', 
            'drop_off_photos', 
            'pick_up_odometer', 
            'drop_off_odometer', 
            'pick_up_note', 
            'drop_off_note', 
            'front_photo',
            'rear_photo',
            'left_photo',
            'right_photo',
            'odometer_photo',
            'optional_photo',
            'drop_off_front_photo',
            'drop_off_rear_photo',
            'drop_off_left_photo',
            'drop_off_right_photo',
            'drop_off_odometer_photo',
            'drop_off_optional_photo',
            #'created_at', 
            #'updated_at'
            ]
'''
from rest_framework import serializers

from rest_framework import serializers

class TripSerializer(serializers.ModelSerializer):
    driver = UserSerializer(read_only=True)
    car = CarSerializer(read_only=True)  # Use the CarSerializer for car details

    pick_up_photos = serializers.SerializerMethodField()
    drop_off_photos = serializers.SerializerMethodField()
    fuel_details = serializers.SerializerMethodField()

    class Meta:
        model = Trip
        fields = [
            'trip_id', 
            'driver', 
            'car', 
            'status', 
            'pick_up_time', 
            'pick_up_location', 
            'drop_off_time', 
            'drop_off_location', 
            'pick_up_photos', 
            'fuel_details', 
            'trip_details', 
            'drop_off_photos', 
            'pick_up_odometer', 
            'drop_off_odometer', 
            'pick_up_note', 
            'drop_off_note', 
            'front_photo',
            'rear_photo',
            'left_photo',
            'right_photo',
            'odometer_photo',
            'optional_photo',
            'drop_off_front_photo',
            'drop_off_rear_photo',
            'drop_off_left_photo',
            'drop_off_right_photo',
            'drop_off_odometer_photo',
            'drop_off_optional_photo',
        ]

    def get_pick_up_photos(self, obj):
        request = self.context.get('request')
        if obj.pick_up_photos:
            return {key: request.build_absolute_uri(url) for key, url in obj.pick_up_photos.items()}
        return {}

    def get_drop_off_photos(self, obj):
        request = self.context.get('request')
        if obj.drop_off_photos:
            return {key: request.build_absolute_uri(url) for key, url in obj.drop_off_photos.items()}
        return {}

    def get_fuel_details(self, obj):
        request = self.context.get('request')
        if obj.fuel_details:
            for entry in obj.fuel_details:
                entry['fuel_receipt_photo'] = request.build_absolute_uri(entry['fuel_receipt_photo'])
            return obj.fuel_details
        return []



class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'address', 'phone_number']