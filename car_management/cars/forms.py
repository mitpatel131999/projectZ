from django import forms
from .models import Car

class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = [ 'owner','car_id','model', 'license_plate','available']
