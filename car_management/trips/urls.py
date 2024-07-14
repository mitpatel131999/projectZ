from django.urls import path
from . import views

urlpatterns = [
   
    path('api/start_trip/', views.StartTripAPI.as_view(), name='start-trip'),
    path('api/add_fuel/', views.AddFuelDetailsAPI.as_view(), name='add-fuel'),
    path('api/complete_trip/', views.CompleteTripAPI.as_view(), name='complete-trip'),
    path('api/drop_off/', views.DropOffCarAPI.as_view(), name='drop-off'),
    path('api/check_ongoing_trip/', views.CheckOngoingTripAPI.as_view(), name='check_ongoing_trip'),

]
