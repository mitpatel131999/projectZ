from django.urls import path
from . import views

urlpatterns = [
    path('api/cars/', views.CarListCreateAPI.as_view(), name='car-list-create'),
    path('api/cars/<int:pk>/', views.CarDetailAPI.as_view(), name='car-detail'),
]
