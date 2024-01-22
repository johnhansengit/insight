from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserSettings, DailyEntry


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

class DailyEntryForm(forms.ModelForm):
    def __init__(self, *args, user_settings=None, **kwargs):
        super(DailyEntryForm, self).__init__(*args, **kwargs)
        labels = {
            "has_had_counseling": "Counseling",
            "has_engaged_spiritually": "Spiritual",
            "sleep_quality_rating": "Sleep",
            "stress_rating": "Stress",
            "physical_health_rating": "Physical Health",
            "has_taken_meds": "Medication",
            "has_gotten_sunshine": "Sunshine",
            "has_eaten_healthily": "Eat healthy",
            "has_connected_socially": "Social Connection",
            "has_exercised": "Exercise",
            "has_used_substances": "Use Substances",
            "has_properly_hydrated": "Hydrate",
            "has_menstruated": "Menstruate",
        }
        widgets = {
            "sleep_quality_rating": forms.NumberInput(
                attrs={
                    "type": "range",
                    "min": 1,
                    "max": 5,
                    "step": 1,
                    "class": "slider-input",
                    "id": "sleep-quality-slider",
                }
            ),
            "stress_rating": forms.NumberInput(
                attrs={
                    "type": "range",
                    "min": 1,
                    "max": 10,
                    "step": 1,
                    "class": "slider-input",
                    "id": "stress-rating-slider",
                }
            ),
            "physical_health_rating": forms.NumberInput(
                attrs={
                    "type": "range",
                    "min": 1,
                    "max": 10,
                    "step": 1,
                    "class": "slider-input",
                    "id": "physical-health-slider",
                }
            ),
            "has_taken_meds": forms.CheckboxInput(
                attrs={"class": "checkbox-input", "id": "has-taken-meds-checkbox"}
            ),
            "has_gotten_sunshine": forms.CheckboxInput(
                attrs={"class": "checkbox-input", "id": "has-gotten-sunshine-checkbox"}
            ),
            "has_eaten_healthily": forms.CheckboxInput(
                attrs={"class": "checkbox-input", "id": "has-eaten-healthily-checkbox"}
            ),
            "has_connected_socially": forms.CheckboxInput(
                attrs={
                    "class": "checkbox-input",
                    "id": "has-connected-socially-checkbox",
                }
            ),
            "has_exercised": forms.CheckboxInput(
                attrs={"class": "checkbox-input", "id": "has-exercised-checkbox"}
            ),
            "has_used_substances": forms.CheckboxInput(
                attrs={"class": "checkbox-input", "id": "has-used-substances-checkbox"}
            ),
            "has_had_counseling": forms.CheckboxInput(
                attrs={"class": "checkbox-input", "id": "has-had-counseling-checkbox"}
            ),
            "has_properly_hydrated": forms.CheckboxInput(
                attrs={
                    "class": "checkbox-input",
                    "id": "has-properly-hydrated-checkbox",
                }
            ),
            "has_engaged_spiritually": forms.CheckboxInput(
                attrs={
                    "class": "checkbox-input",
                    "id": "has-engaged-spiritually-checkbox",
                }
            ),
            "has_menstruated": forms.CheckboxInput(
                attrs={"class": "checkbox-input", "id": "has-menstruated-checkbox"}
            ),
        }
        if user_settings:
            included_fields = {
                "has_had_counseling": user_settings.track_counseling,
                "has_engaged_spiritually": user_settings.track_spirituality,
                "sleep_quality_rating": user_settings.track_sleep,
                "stress_rating": user_settings.track_stress,
                "physical_health_rating": user_settings.track_physical_health,
                "has_taken_meds": user_settings.track_meds,
                "has_gotten_sunshine": user_settings.track_sunshine,
                "has_eaten_healthily": user_settings.track_eating_healthily,
                "has_connected_socially": user_settings.track_connecting_socially,
                "has_exercised": user_settings.track_exercise,
                "has_used_substances": user_settings.track_substances,
                "has_properly_hydrated": user_settings.track_hydrated,
                "has_menstruated": user_settings.track_menstruation,
            }
            for field_name, field_value in included_fields.items():
                if not field_value:
                    del self.fields[field_name]
    
    class Meta:
        model = DailyEntry
        exclude = ["user"]
        labels = {
            "has_had_counseling": "Counseling",
            "has_engaged_spiritually": "Spiritual",
            "sleep_quality_rating": "Sleep",
            "stress_rating": "Stress",
            "physical_health_rating": "Physical Health",
            "has_taken_meds": "Medication",
            "has_gotten_sunshine": "Sunshine",
            "has_eaten_healthily": "Eat healthy",
            "has_connected_socially": "Social Connection",
            "has_exercised": "Exercise",
            "has_used_substances": "Use Substances",
            "has_hydrated": "Hydrate",
            "has_menstruated": "Menstruate",
        }
        widgets = {
            "sleep_quality_rating": forms.NumberInput(
                attrs={
                    "type": "range",
                    "min": 1,
                    "max": 5,
                    "step": 1,
                    "class": "slider-input",
                    "id": "sleep-quality-slider",
                }
            ),
            "stress_rating": forms.NumberInput(
                attrs={
                    "type": "range",
                    "min": 1,
                    "max": 10,
                    "step": 1,
                    "class": "slider-input",
                    "id": "stress-rating-slider",
                }
            ),
            "physical_health_rating": forms.NumberInput(
                attrs={
                    "type": "range",
                    "min": 1,
                    "max": 10,
                    "step": 1,
                    "class": "slider-input",
                    "id": "physical-health-slider",
                }
            ),
            "has_taken_meds": forms.CheckboxInput(
                attrs={"class": "checkbox-input", "id": "has-taken-meds-checkbox"}
            ),
            "has_gotten_sunshine": forms.CheckboxInput(
                attrs={"class": "checkbox-input", "id": "has-gotten-sunshine-checkbox"}
            ),
            "has_eaten_healthily": forms.CheckboxInput(
                attrs={"class": "checkbox-input", "id": "has-eaten-healthily-checkbox"}
            ),
            "has_connected_socially": forms.CheckboxInput(
                attrs={
                    "class": "checkbox-input",
                    "id": "has-connected-socially-checkbox",
                }
            ),
            "has_exercised": forms.CheckboxInput(
                attrs={"class": "checkbox-input", "id": "has-exercised-checkbox"}
            ),
            "has_used_substances": forms.CheckboxInput(
                attrs={"class": "checkbox-input", "id": "has-used-substances-checkbox"}
            ),
            "has_had_counseling": forms.CheckboxInput(
                attrs={"class": "checkbox-input", "id": "has-had-counseling-checkbox"}
            ),
            "has_properly_hydrated": forms.CheckboxInput(
                attrs={
                    "class": "checkbox-input",
                    "id": "has-properly-hydrated-checkbox",
                }
            ),
            "has_engaged_spiritually": forms.CheckboxInput(
                attrs={
                    "class": "checkbox-input",
                    "id": "has-engaged-spiritually-checkbox",
                }
            ),
            "has_menstruated": forms.CheckboxInput(
                attrs={"class": "checkbox-input", "id": "has-menstruated-checkbox"}
            ),
        }