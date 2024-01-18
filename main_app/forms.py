from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=100, help_text="First Name")
    last_name = forms.CharField(max_length=100, help_text="Last Name")
    email = forms.EmailField(max_length=254, help_text="Email")

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
