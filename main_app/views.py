from datetime import date, timedelta
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from .forms import SignUpForm
from .models import UserSettings, DailyEntry, Emotion


# Create your views here.
def home(request):
    return render(request, "home.html")


def sandbox(request):
    return render(request, "sandbox.html")


def timeline(request):
    daily_entries = DailyEntry.objects.filter(user=request.user.profile).prefetch_related('emotion')

    if not daily_entries.exists():
        return render(request, "timeline.html", {})

    oldest_entry = daily_entries.earliest('date').date
    today = date.today()
    delta = today - oldest_entry
    date_list = [today - timedelta(days=i) for i in range(delta.days + 1)]

    emotion_categories = Emotion.objects.filter(
        parent__isnull=False, 
        parent__parent__isnull=True
    ).values_list('name', flat=True).distinct()

    emotions_by_date = {}
    for entry in daily_entries:
        emotion_set = set()
        for emotion in entry.emotion.all():
            emotion_set.add(emotion.name)
            if emotion.parent:
                emotion_set.add(emotion.parent.name)
        emotions_by_date[entry.date] = emotion_set

    return render(request, "timeline.html", {
        'date_list': date_list,
        'emotion_categories': emotion_categories,
        'emotions_by_date': emotions_by_date,
    })


def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            user.profile.email = form.cleaned_data.get("email")
            user.profile.first_name = form.cleaned_data.get("first_name")
            user.profile.last_name = form.cleaned_data.get("last_name")
            user.save()
            login(request, user)
            return redirect("home")
    form = SignUpForm()
    context = {"form": form}
    return render(request, "registration/signup.html", context)


# User Settings Views
class UserSettingsCreate(CreateView):
    model = UserSettings
    
    
class UserSettingsRead(DetailView):
    model = UserSettings
    
    
class UserSettingsUpdate(UpdateView):
    model = UserSettings

# Daily Entry Views
class DailyEntryList(ListView):
    model = DailyEntry


class DailyEntryCreate(CreateView):
    model = DailyEntry


class DailyEntryRead(DetailView):
    model = DailyEntry


class DailyEntryUpdate(UpdateView):
    model = DailyEntry


class DailyEntryDelete(DeleteView):
    model = DailyEntry
    success_url = '/daily-entries'

