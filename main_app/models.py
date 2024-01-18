from django.db import models
from django.utils import timezone

# auth imports
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField(max_length=254)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()


class Emotion(models.Model):
    name = models.CharField(max_length=20)
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)
    color = models.CharField(max_length = 20)
    
    def __str__(self):
        return self.name


class DailyEntry(models.Model):
    sleep_quality_rating = models.IntegerField(null=True, blank=True)
    stress_rating = models.IntegerField(null=True, blank=True)
    physical_health_rating = models.IntegerField(null=True, blank=True)
    has_taken_meds = models.BooleanField(null=True, blank=True)
    has_gotten_sunshine = models.BooleanField(null=True, blank=True)
    has_eaten_healthily = models.BooleanField(null=True, blank=True)
    has_connected_socially = models.BooleanField(null=True, blank=True)
    has_exercised = models.BooleanField(null=True, blank=True)
    has_used_substances = models.BooleanField(null=True, blank=True)
    has_had_counseling = models.BooleanField(null=True, blank=True)
    has_properly_hydrated = models.BooleanField(null=True, blank=True)
    has_engaged_spiritually = models.BooleanField(null=True, blank=True)
    has_menstruated = models.BooleanField(null=True, blank=True)
    journal_entry = models.TextField(null=True, blank=True)
    date = models.DateField(default=timezone.now)

    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='entries')
    emotion = models.ManyToManyField(Emotion)
    
    def __str__(self):
        return f"Entry for {self.date}"
    
    
class UserSettings(models.Model):
    track_counseling = models.BooleanField(default=False)
    track_spirituality = models.BooleanField(default=False)
    track_sleep = models.BooleanField(default=False)
    track_stress = models.BooleanField(default=False)
    track_physical_health = models.BooleanField(default=False)
    track_meds = models.BooleanField(default=False)
    track_sunshine = models.BooleanField(default=False)
    track_eating_healthily = models.BooleanField(default=False)
    track_connecting_socially = models.BooleanField(default=False)
    track_exercise = models.BooleanField(default=False)
    track_substances = models.BooleanField(default=False)
    track_hydrated = models.BooleanField(default=False)
    track_menstruation = models.BooleanField(default=False)
    
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='user_settings')
    
    def __str__(self):
        return f"{self.user.first_name}'s settings | ID: {self.id}"
    
