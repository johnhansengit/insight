from datetime import date, timedelta
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.http import JsonResponse
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView, View
from .forms import SignUpForm
from .models import UserSettings, DailyEntry, Emotion


# Create your views here.
def home(request):
    return render(request, "home.html")


def sandbox(request):
    return render(request, "sandbox.html")


def timeline(request):
    daily_entries = DailyEntry.objects.filter(user_id=request.user.id).prefetch_related('emotion')

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

    emotions_by_date = []
    for entry_date in date_list:
        emotion_dict = {emotion: False for emotion in emotion_categories}
        for entry in daily_entries.filter(date=entry_date):
            for emotion in entry.emotion.all():
                if emotion.name in emotion_dict:
                    emotion_dict[emotion.name] = True
                if emotion.parent and emotion.parent.name in emotion_dict:
                    emotion_dict[emotion.parent.name] = True
        emotions_by_date.append({'date': entry_date, 'emotions': emotion_dict})


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

# Emotions Views
class EmotionsDataView(View):
    def get(self, request):
        # Step 1: Query all Emotion objects with no parent (top-level emotions)
        top_level_emotions = Emotion.objects.filter(parent__isnull=True)

        # Step 2 & 3: For each top-level emotion, get its children and their children
        emotions_data = [self.get_emotion_data(emotion) for emotion in top_level_emotions]

        return JsonResponse(emotions_data, safe=False)

    def get_emotion_data(self, emotion):
        data = {
            'name': emotion.name,
            'color': emotion.color,
            'timeline_color': emotion.timeline_color,
            'children': [self.get_emotion_data(child) for child in Emotion.objects.filter(parent=emotion.id)]
        }
        return data
    
