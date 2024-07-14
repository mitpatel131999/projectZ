from django.db import models
from profiles.models import User

class Car(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_cars')
    car_id = models.AutoField(primary_key=True)
    model = models.CharField(max_length=100)
    license_plate = models.CharField(max_length=20)
    available = models.BooleanField(default=True)

