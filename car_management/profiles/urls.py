from django.urls import path
from . import views
from .views import RegisterAPI, LoginAPI

urlpatterns = [
   
    path('api/register/', views.RegisterAPI.as_view(), name='api-register'),
    path('api/login/', views.LoginAPI.as_view(), name='api-login'),
    path('api/logout/', views.LogoutAPI.as_view(), name='api-logout'),
    path('api/cars/', views.CarListCreateAPI.as_view(), name='api-cars'),
    path('api/cars/<int:pk>/', views.CarDetailAPI.as_view(), name='api-car-detail'),
    path('api/trips/', views.TripListCreateAPI.as_view(), name='api-trips'),
    path('api/trips/<int:pk>/', views.TripDetailAPI.as_view(), name='api-trip-detail'),
    path('api/approve_driver/<int:driver_id>/', views.ApproveDriverAPI.as_view(), name='api-approve-driver'),

    path('api/make_admin/<int:user_id>/', views.MakeAdminAPI.as_view(), name='make-admin'),
    path('api/drivers/', views.DriverProfileListAPI.as_view(), name='api-drivers'),
    path('api/car_owner/', views.CarOwnerProfileListAPI.as_view(), name='api-drivers'),
    path('api/profile/', views.UserProfileUpdateAPI.as_view(), name='api-update-profile'),
    
    
    

]
