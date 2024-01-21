from datetime import date, timedelta
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView, View
from django.shortcuts import get_object_or_404
from .forms import SignUpForm, UserSettingsForm
from .models import UserSettings, DailyEntry, Emotion, Profile
from django.urls import reverse_lazy


# Create your views here.
@login_required
def home(request):
    return render(request, "home.html", {'title': 'Welcome'})


def sandbox(request):
    return render(request, "sandbox.html")

@login_required
def timeline(request):
    # Get emotion categories for table header
    emotion_categories = Emotion.objects.filter(
        parent__isnull=False, 
        parent__parent__isnull=True
    )
    
    # Get user settings for dropdown
    user_settings = UserSettings.objects.filter(user=request.user.id).first()
    
    settings_mapping = {
    'Counseling': ['track_counseling', 'has_had_counseling'],
    'Spirituality': ['track_spirituality', 'has_engaged_spiritually'],
    'Sleep': ['track_sleep', 'sleep_quality_rating'],
    'Stress': ['track_stress', 'stress_rating'],
    'Physical Health': ['track_physical_health', 'physical_health_rating'],
    'Medication': ['track_meds', 'has_taken_meds'],
    'Sunshine': ['track_sunshine', 'has_gotten_sunshine'],
    'Ate Healthy': ['track_eating_healthily', 'has_eaten_healthily'],
    'Connected': ['track_connecting_socially', 'has_connected_socially'],
    'Exercise': ['track_exercise', 'has_exercised'],
    'Substances': ['track_substances', 'has_used_substances'],
    'Hydrated': ['track_hydrated', 'has_properly_hydrated'],
    'Menstruation': ['track_menstruation', 'has_menstruated']
    }

    tracked_lifestyles = []

    if user_settings:
        for friendly_term, field_names in settings_mapping.items():
            for field_name in field_names:
                if getattr(user_settings, field_name, False):
                    tracked_lifestyles.append(friendly_term)
                    break
    
    # Get selected lifestyle from form
    selected_lifestyle = request.POST.get('lifestyle-selector', '')
    
    # Get user data for tables
    daily_entries = DailyEntry.objects.filter(user=request.user.id)
    
    render_timeline = daily_entries.exists()

    oldest_entry = daily_entries.order_by('date').first()
    today = date.today()
    delta = today - oldest_entry.date  # Make sure to use the date field
    date_list = [today - timedelta(days=i) for i in range(delta.days + 1)]

    emotions_by_date = []
    lifestyle_by_date = []

    for entry_date in date_list:
        emotion_set = set()

        for entry in daily_entries.filter(date=entry_date):
            for emotion in entry.emotion.all():
                if emotion.parent.parent is None:
                    emotion_set.add(emotion.name)
                else:
                    emotion_set.add(emotion.parent.name)

            for friendly_term, field_names in settings_mapping.items():
                if selected_lifestyle == friendly_term:
                    lifestyle_by_date.append({'date': entry_date, 'lifestyle': friendly_term, 'value': getattr(entry, field_names[1], None)})
                    break

        emotions_by_date.append({'date': entry_date, 'emotions': list(emotion_set)})

    return render(request, "timeline.html", {
        'date_list': date_list,
        'emotion_categories': emotion_categories,
        'emotions_by_date': emotions_by_date,
        'render_timeline': render_timeline,
        'tracked_lifestyles': tracked_lifestyles,
        'selected_lifestyle': selected_lifestyle,
        'lifestyle_by_date': lifestyle_by_date,
        'title': 'Timeline'
    })


def process_lifestyle_selector(request):
    if request.method == 'POST':
        return timeline(request)
    else:
        return redirect('timeline')
    

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

# User Settings Views
class UserSettingsUpdate(LoginRequiredMixin, UpdateView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.title is not None:
            context['title'] = self.title
        return context

class UserSettingsRead(LoginRequiredMixin, TitleMixin, DetailView):
    model = UserSettings
    title = 'Settings'
    template_name = 'main_app/user-settings.html'

    def get_object(self):
        """ Override to get the settings object for the current user. """
        profile = get_object_or_404(Profile, user=self.request.user)
        return get_object_or_404(UserSettings, user=profile)
    
class UserSettingsUpdate(LoginRequiredMixin, TitleMixin, UpdateView):
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
class DailyEntryList(LoginRequiredMixin, TitleMixin, ListView):
    model = DailyEntry
    title = 'Log'


class DailyEntryCreate(LoginRequiredMixin, TitleMixin, CreateView):
    model = DailyEntry
    title = 'Log'


class DailyEntryRead(LoginRequiredMixin, TitleMixin, DetailView):
    title = 'Log'
    model = DailyEntry
    template_name = 'daily_entries/detail.html'
    success_url = reverse_lazy('daily_entry_detail')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_settings'] = UserSettings.objects.filter(user_id=self.request.user.id).first()
        return context


class DailyEntryUpdate(LoginRequiredMixin, TitleMixin, UpdateView):
    model = DailyEntry
    title = 'Log'


class DailyEntryDelete(LoginRequiredMixin, DeleteView):
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
