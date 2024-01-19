from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserSettings


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    email = forms.EmailField(max_length=254)

    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "email",
            "username",
            "password1",
            "password2",
        ]

class UserSettingsForm(forms.ModelForm):
    class Meta:
        model = UserSettings
        fields = [
            'track_counseling', 'track_spirituality', 'track_sleep', 'track_stress', 
            'track_physical_health', 'track_meds', 'track_sunshine', 'track_eating_healthily', 
            'track_connecting_socially', 'track_exercise', 'track_substances', 
            'track_hydrated', 'track_menstruation'
        ]