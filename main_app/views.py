from datetime import date, timedelta
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView, View
from django.shortcuts import get_object_or_404
from .forms import SignUpForm, UserSettingsForm
from .models import UserSettings, DailyEntry, Emotion, Profile


# Create your views here.
def home(request):
    return render(request, "home.html", {'title': 'Welcome'})


def sandbox(request):
    return render(request, "sandbox.html")


def timeline(request):
    emotion_categories = Emotion.objects.filter(
        parent__isnull=False, 
        parent__parent__isnull=True
    )
    
    daily_entries = DailyEntry.objects.filter(user=request.user.id)
    
    if daily_entries.exists():
        render_timeline = True;
    else:
        render_timeline = False;

    oldest_entry = daily_entries.order_by('date').first()
    today = date.today()
    delta = today - oldest_entry.date  # Make sure to use the date field
    date_list = [today - timedelta(days=i) for i in range(delta.days + 1)]

    emotions_by_date = []
    for entry_date in date_list:
        emotion_set = set()
        for entry in daily_entries.filter(date=entry_date):
            for emotion in entry.emotion.all():
                if emotion.parent.parent is None:
                    emotion_set.add(emotion.name)
                else:
                    emotion_set.add(emotion.parent.name)
        emotions_by_date.append({'date': entry_date, 'emotions': list(emotion_set)})

    return render(request, "timeline.html", {
        'date_list': date_list,
        'emotion_categories': emotion_categories,
        'emotions_by_date': emotions_by_date,
        'render_timeline': render_timeline,
        'title': 'Timeline'
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

# Mixins
class TitleMixin:
    title = None
    
    def get_context_data(self, **kwargs):
        # First, get the existing context from the superclass
        context = super().get_context_data(**kwargs)
        
        # Add the title to the context
        context['title'] = self.title
        
        # Return the updated context
        return context

# User Settings Views
class UserSettingsUpdate(UpdateView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.title is not None:
            context['title'] = self.title
        return context

# User Settings Views   
class UserSettingsRead(TitleMixin, DetailView):
    model = UserSettings
    title = 'Settings'
    template_name = 'main_app/user-settings.html'

    def get_object(self):
        """ Override to get the settings object for the current user. """
        profile = get_object_or_404(Profile, user=self.request.user)
        return get_object_or_404(UserSettings, user=profile)
    
    
class UserSettingsUpdate(TitleMixin, UpdateView):
    model = UserSettings
    title = 'Settings'
    form_class = UserSettingsForm
    template_name = 'main_app/user-settings-form.html'
    success_url = '/'

    def get_object(self):
        """ Override to get the settings object for the current user. """
        profile = get_object_or_404(Profile, user=self.request.user)
        return get_object_or_404(UserSettings, user=profile)

# Daily Entry Views
class DailyEntryList(TitleMixin, ListView):
    model = DailyEntry
    title = 'Log'


class DailyEntryCreate(TitleMixin, CreateView):
    model = DailyEntry
    title = 'Log'


class DailyEntryRead(TitleMixin, DetailView):
    model = DailyEntry
    title = 'Log'


class DailyEntryUpdate(TitleMixin, UpdateView):
    model = DailyEntry
    title = 'Log'


class DailyEntryDelete(DeleteView):
    model = DailyEntry
    success_url = '/daily-entries'

# Journal Views
class JournalEntryList(LoginRequiredMixin, TitleMixin, ListView):
    model = DailyEntry
    template_name = 'main_app/journal-entries-list.html' 
    title = 'Journal Entries'
    context_object_name = 'entries'  # Name of the context variable in the template

    def get_queryset(self):
        """ Override to get journal entries for the current user. """
        return DailyEntry.objects.filter(user__user=self.request.user).order_by('-date')

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
