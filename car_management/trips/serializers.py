from rest_framework import serializers
from .models import Trip
from cars.models import Car


class CarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = '__all__'


from rest_framework import serializers
from .models import Trip, Car


class TripSerializer(serializers.ModelSerializer):
    driver = serializers.ReadOnlyField(source='driver.username')
    car = serializers.StringRelatedField(read_only=True)

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

