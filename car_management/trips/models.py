from django.db import models
from profiles.models import User
from cars.models import Car

from django.utils import timezone

from django.db import models
from django.utils import timezone
from profiles.models import User
from cars.models import Car

class Trip(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    )
    trip_id = models.AutoField(primary_key=True)
    driver = models.ForeignKey(User, on_delete=models.CASCADE)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    status = models.CharField(max_length=255, choices=STATUS_CHOICES, default='pending')
    pick_up_photos = models.JSONField()
    drop_off_photos = models.JSONField(null=True, blank=True)
    pick_up_odometer = models.CharField(max_length=255)
    drop_off_odometer = models.CharField(max_length=255, null=True, blank=True)
    pick_up_time = models.DateTimeField()
    drop_off_time = models.DateTimeField(null=True, blank=True)
    pick_up_location = models.CharField(max_length=255)
    drop_off_location = models.CharField(max_length=255, null=True, blank=True)
    pick_up_note = models.TextField(blank=True, null=True)
    drop_off_note = models.TextField(blank=True, null=True)
    front_photo = models.ImageField(upload_to='photos/', null=True, blank=True)
    rear_photo = models.ImageField(upload_to='photos/', null=True, blank=True)
    left_photo = models.ImageField(upload_to='photos/', null=True, blank=True)
    right_photo = models.ImageField(upload_to='photos/', null=True, blank=True)
    odometer_photo = models.ImageField(upload_to='photos/', null=True, blank=True)
    optional_photo = models.ImageField(upload_to='photos/', null=True, blank=True)
    drop_off_front_photo = models.ImageField(upload_to='photos/', null=True, blank=True)
    drop_off_rear_photo = models.ImageField(upload_to='photos/', null=True, blank=True)
    drop_off_left_photo = models.ImageField(upload_to='photos/', null=True, blank=True)
    drop_off_right_photo = models.ImageField(upload_to='photos/', null=True, blank=True)
    drop_off_odometer_photo = models.ImageField(upload_to='photos/', null=True, blank=True)
    drop_off_optional_photo = models.ImageField(upload_to='photos/', null=True, blank=True)
    fuel_details = models.JSONField(default=list, blank=True)  # To store multiple fuel entries
    trip_details = models.JSONField(null=True, blank=True)
    #created_at = models.DateTimeField(auto_now_add=True)
    #updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Trip {self.trip_id} by {self.driver.username}"
