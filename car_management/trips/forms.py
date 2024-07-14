from django import forms
from .models import Trip

class TripForm(forms.ModelForm):
    class Meta:
        model = Trip
        fields = ['car', 'odometer_reading_start', 'notes_start', 'pick_up_photos']
