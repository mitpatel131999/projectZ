from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.utils import timezone
from .models import Trip, Car
from .serializers import TripSerializer, CarSerializer
from rest_framework.authentication import TokenAuthentication

import os
import uuid
from django.core.files.storage import default_storage
from rest_framework.views import APIView

class CheckOngoingTripAPI(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get(self, request, *args, **kwargs):
        ongoing_trip = Trip.objects.filter(driver=request.user, status='in_progress').first()
        if ongoing_trip:
            return Response({"trip_id": ongoing_trip.trip_id, "status": "in_progress"}, status=status.HTTP_200_OK)
        else:
            return Response({"status": "no_ongoing_trip"}, status=status.HTTP_200_OK)

def save_uploaded_file(uploaded_file, prefix):
    extension = os.path.splitext(uploaded_file.name)[1]
    unique_filename = f"{prefix}_{uuid.uuid4().hex}{extension}"
    path = default_storage.save(f'photos/{unique_filename}', uploaded_file)
    return default_storage.url(path)

class StartTripAPI(generics.CreateAPIView):
    serializer_class = TripSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def post(self, request, *args, **kwargs):
        # Check if the driver already has an active trip
        active_trip = Trip.objects.filter(driver=request.user, status='in_progress').first()
        if active_trip:
            return Response({"error": "You already have an active trip."}, status=status.HTTP_400_BAD_REQUEST)
        
        car_id = request.data.get('car_id')
        car = get_object_or_404(Car, car_id=car_id, available=True)
        front_photo = request.FILES.get('front_photo')
        rear_photo = request.FILES.get('rear_photo')
        left_photo = request.FILES.get('left_photo')
        right_photo = request.FILES.get('right_photo')
        odometer_photo = request.FILES.get('odometer_photo')
        optional_photo = request.FILES.get('optional_photo')
        pick_up_odometer = request.data.get('pick_up_odometer')
        pick_up_location = request.data.get('pick_up_location')
        pick_up_note = request.data.get('pick_up_note')
        pick_up_time = timezone.now()

        # Check for required photos and fields
        if not all([front_photo, rear_photo, left_photo, right_photo, odometer_photo]):
            return Response({"error": "All 5 pickup photos (4 car photos and 1 odometer photo) are required."}, status=status.HTTP_400_BAD_REQUEST)
        if not pick_up_odometer or not pick_up_location:
            return Response({"error": "Pickup odometer and location are required."}, status=status.HTTP_400_BAD_REQUEST)

        # Save files with unique names and get their URLs
        pick_up_photos = {
            'front': save_uploaded_file(front_photo, f"{car_id}_front"),
            'rear': save_uploaded_file(rear_photo, f"{car_id}_rear"),
            'left': save_uploaded_file(left_photo, f"{car_id}_left"),
            'right': save_uploaded_file(right_photo, f"{car_id}_right"),
            'odometer': save_uploaded_file(odometer_photo, f"{car_id}_odometer"),
            'optional': save_uploaded_file(optional_photo, f"{car_id}_optional"),
        }

        trip = Trip.objects.create(
            driver=request.user,
            car=car,
            status='in_progress',
            pick_up_photos=pick_up_photos,
            pick_up_odometer=pick_up_odometer,
            pick_up_time=pick_up_time,
            pick_up_location=pick_up_location,
            pick_up_note=pick_up_note
        )

        car.available = False
        car.save()
        
        return Response({"message": "Trip started successfully", "trip_id": trip.trip_id}, status=status.HTTP_201_CREATED)

class DropOffCarAPI(generics.UpdateAPIView):
    serializer_class = TripSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def post(self, request, *args, **kwargs):
        trip_id = request.data.get('trip_id')
        trip = get_object_or_404(Trip, trip_id=trip_id, status='in_progress')
        drop_off_front_photo = request.FILES.get('drop_off_front_photo')
        drop_off_rear_photo = request.FILES.get('drop_off_rear_photo')
        drop_off_left_photo = request.FILES.get('drop_off_left_photo')
        drop_off_right_photo = request.FILES.get('drop_off_right_photo')
        drop_off_odometer_photo = request.FILES.get('drop_off_odometer_photo')
        drop_off_optional_photo = request.FILES.get('drop_off_optional_photo')
        drop_off_odometer = request.data.get('drop_off_odometer')
        drop_off_location = request.data.get('drop_off_location')
        drop_off_note = request.data.get('drop_off_note')
        drop_off_time = timezone.now()

        # Check for required photos and fields
        if not all([drop_off_front_photo, drop_off_rear_photo, drop_off_left_photo, drop_off_right_photo, drop_off_odometer_photo]):
            return Response({"error": "All 5 drop-off photos (4 car photos and 1 odometer photo) are required."}, status=status.HTTP_400_BAD_REQUEST)
        if not drop_off_odometer or not drop_off_location:
            return Response({"error": "Drop-off odometer and location are required."}, status=status.HTTP_400_BAD_REQUEST)

        # Save files with unique names and get their URLs
        drop_off_photos = {
            'front': save_uploaded_file(drop_off_front_photo, f"{trip.car.car_id}_drop_off_front"),
            'rear': save_uploaded_file(drop_off_rear_photo, f"{trip.car.car_id}_drop_off_rear"),
            'left': save_uploaded_file(drop_off_left_photo, f"{trip.car.car_id}_drop_off_left"),
            'right': save_uploaded_file(drop_off_right_photo, f"{trip.car.car_id}_drop_off_right"),
            'odometer': save_uploaded_file(drop_off_odometer_photo, f"{trip.car.car_id}_drop_off_odometer"),
            'optional': save_uploaded_file(drop_off_optional_photo, f"{trip.car.car_id}_drop_off_optional") if drop_off_optional_photo else None,
        }

        # Calculate total distance
        total_distance = int(drop_off_odometer) - int(trip.pick_up_odometer)

        trip.status = 'completed'
        trip.drop_off_photos = drop_off_photos
        trip.drop_off_odometer = drop_off_odometer
        trip.drop_off_time = drop_off_time
        trip.drop_off_location = drop_off_location
        trip.drop_off_note = drop_off_note
        trip.total_distance = total_distance
        trip.save()

        car = trip.car
        car.available = True
        car.save()
        
        return Response({"message": "Trip completed successfully", "total_distance": total_distance}, status=status.HTTP_200_OK)


class AddFuelDetailsAPI(generics.UpdateAPIView):
    serializer_class = TripSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def post(self, request, *args, **kwargs):
        trip_id = request.data.get('trip_id')
        trip = get_object_or_404(Trip,  trip_id=trip_id, driver=request.user)
        if trip.status != 'in_progress':
            return Response({"error": "Trip is not in progress."}, status=status.HTTP_400_BAD_REQUEST)

        fuel_receipt_photo = request.FILES.get('fuel_receipt_photo')
        fuel_amount = int(request.data.get('fuel_amount'))
        note = request.data.get('note')
        
        if not fuel_receipt_photo or not fuel_amount:
            return Response({"error": "Fuel amount and receipt photo are required."}, status=status.HTTP_400_BAD_REQUEST)

        fuel_entry = {
            'fuel_amount': fuel_amount,
            'fuel_receipt_photo': save_uploaded_file(fuel_receipt_photo, f"{trip.car.car_id}_fuel_receipt"),
            'note': note
        }

        if not trip.fuel_details:
            trip.fuel_details = []

        trip.fuel_details.append(fuel_entry)
        trip.save()

        return Response(TripSerializer(trip).data, status=status.HTTP_200_OK)


class CompleteTripAPI(generics.UpdateAPIView):
    serializer_class = TripSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def post(self, request, *args, **kwargs):
        trip_id = request.data.get('trip_id')
        trip = get_object_or_404(Trip, trip_id=trip_id, driver=request.user)
        if trip.status != 'in_progress':
            return Response({"error": "Trip is not in progress."}, status=status.HTTP_400_BAD_REQUEST)

        trip_details = {
            'route_no': request.data.get('route_no'),
            'total_deliveries': request.data.get('total_deliveries'),
            'return_deliveries': request.data.get('return_deliveries'),
            'successful_deliveries': request.data.get('successful_deliveries'),
            'note': request.data.get('note')
        }

        if not trip_details['route_no'] or not trip_details['total_deliveries'] or not trip_details['return_deliveries'] or not trip_details['successful_deliveries']:
            return Response({"error": "All trip details are required."}, status=status.HTTP_400_BAD_REQUEST)

        trip.trip_details = trip_details
        trip.total_distance = None  # Set total distance to null
        #trip.status = 'completed'  # Mark the trip as completed
        trip.save()

        return Response(TripSerializer(trip).data, status=status.HTTP_200_OK)
