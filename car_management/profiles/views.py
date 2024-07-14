from django.shortcuts import render, redirect
from rest_framework import generics, permissions, status, views as rest_views
from django.contrib.auth import authenticate, login, logout
from .models import User

from cars.models import Car
from trips.models import Trip
from django.shortcuts import get_object_or_404

from .forms import UserRegisterForm, UserLoginForm

from rest_framework import generics, status, views
from rest_framework.response import Response
from rest_framework.permissions import AllowAny,IsAuthenticated,IsAuthenticated
from .serializers import UserRegisterSerializer, UserLoginSerializer, CarSerializer, TripSerializer, UserProfileSerializer
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from django.contrib.auth.decorators import user_passes_test, login_required
from rest_framework.authentication import TokenAuthentication

class RegisterAPI(generics.CreateAPIView):
    serializer_class = UserRegisterSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": UserRegisterSerializer(user, context=self.get_serializer_context()).data,
            "message": "User created successfully.",
        }, status=status.HTTP_201_CREATED)



class LoginAPI(generics.GenericAPIView):
    serializer_class = UserLoginSerializer
    permission_classes = [AllowAny]

    
    def post(self, request, *args, **kwargs):

        ## remove below lines 



        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        
        # Authenticate and login the user
        login(request, user)
        print('User login successfully')
        # Create or get the token
        token, created = Token.objects.get_or_create(user=user)
        
        return Response({
            "token": token.key,
            "user_id": user.pk,
            "email": user.email,
            "role": user.role,
            "message": "User logged in successfully.",
        }, status=status.HTTP_200_OK)
   


class LogoutAPI(rest_views.APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            request.user.auth_token.delete()
            logout(request)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response({"message": "Successfully logged out."}, status=status.HTTP_200_OK)


class CarListCreateAPI(generics.ListCreateAPIView):
    queryset = Car.objects.all()
    serializer_class = CarSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class CarDetailAPI(generics.RetrieveUpdateDestroyAPIView):
    queryset = Car.objects.all()
    serializer_class = CarSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

class IsOwnerOrAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.user.role == 'admin':
            return True
        if request.user.role == 'renter' and obj.owner == request.user:
            return True
        if request.user.role == 'driver' and obj.driver == request.user:
            return True
        return False

class TripListCreateAPI(generics.ListCreateAPIView):
    serializer_class = TripSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'admin':
            return Trip.objects.all().order_by('-pick_up_time')
        elif user.role == 'renter':
            return Trip.objects.filter(car__owner=user).order_by('-pick_up_time')
        elif user.role == 'driver':
            return Trip.objects.filter(driver=user).order_by('-pick_up_time')
        return Trip.objects.none()

    def perform_create(self, serializer):
        car = get_object_or_404(Car, car_id=self.request.data.get('car_id'))
        serializer.save(driver=self.request.user, car=car)
    
class TripDetailAPI(generics.RetrieveUpdateDestroyAPIView):
    queryset = Trip.objects.all()
    serializer_class = TripSerializer
    permission_classes = [IsAuthenticated]

class ApproveDriverAPI(rest_views.APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def post(self, request, driver_id, *args, **kwargs):
        user = get_object_or_404(User, id=driver_id, role='driver')
        user.status = 'approved'
        user.save()
        return Response({"message": "Driver approved successfully."}, status=status.HTTP_200_OK)

class MakeAdminAPI(views.APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def post(self, request, user_id, *args, **kwargs):
        user = get_object_or_404(User, id=user_id)
        if request.user.is_superuser:
            user.role = 'admin'
            user.is_staff = True
            user.is_superuser = True
            user.save()
            return Response({"message": "User promoted to admin successfully."}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "You do not have permission to perform this action."}, status=status.HTTP_403_FORBIDDEN)

class DriverProfileListAPI(generics.ListAPIView):
    queryset = User.objects.filter(role='driver')
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

class CarOwnerProfileListAPI(generics.ListAPIView):
    queryset = User.objects.filter(role='owner')
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

class UserProfileUpdateAPI(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]


    def get_object(self):
        return self.request.user

