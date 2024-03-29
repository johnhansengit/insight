from datetime import date, datetime, timedelta
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView, View
from django.shortcuts import get_object_or_404
from .forms import SignUpForm, UserSettingsForm, DailyEntryForm
from .models import UserSettings, DailyEntry, Emotion, Profile
from django.urls import reverse_lazy, reverse
from .utils import send_gpt_json
import json
import logging
# Configure logging at the beginning of your Django view file
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


# Create your views here.
@login_required
def home(request):
    today = date.today()
    profile = Profile.objects.get(user=request.user)
    existing_entry = DailyEntry.objects.filter(user=profile, date=today).first()

    context = {
        'title': 'Welcome',
        'existing_entry': existing_entry,
        'today': today.strftime("%Y-%m-%d")
    }
    
    return render(request, "home.html", context)


def sandbox(request):
    return render(request, "sandbox.html")

@login_required
def timeline(request):
    profile = Profile.objects.get(user=request.user)

    # Get user data for tables
    daily_entries = DailyEntry.objects.filter(user=profile)
    render_timeline = daily_entries.exists()

    # If no daily entries, skip the rest and return minimal context
    if not render_timeline:
        return render(request, "timeline.html", {
            'render_timeline': render_timeline,
            'title': 'Timeline',
            'title_color': 'var(--accent-pink)'
        })

    # Rest of the code runs only if there are daily entries

    # Get emotion categories for table header
    emotion_categories = Emotion.objects.filter(
        parent__isnull=False, 
        parent__parent__isnull=True
    ).order_by('order')
    
    # Get user settings for dropdown
    user_settings = UserSettings.objects.filter(user=profile).first()
    
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
    
    oldest_entry = daily_entries.order_by('date').first()
    today = date.today()
    delta = today - oldest_entry.date
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
        'title': 'Timeline',
        'title_color': 'var(--accent-pink)'
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
        else:
            return render(request, "registration/signup.html", {"form": form})
    form = SignUpForm()
    context = {"form": form}
    return render(request, "registration/signup.html", context)


# Mixins
class TitleMixin:
    title = None
    title_color = None
    
    def get_context_data(self, **kwargs):
        # First, get the existing context from the superclass
        context = super().get_context_data(**kwargs)
        
        # Add the title to the context
        context['title'] = self.title
        context['title_color'] = self.title_color
        
        # Return the updated context
        return context

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
    title_color = 'var(--accent-purple)'
    template_name = 'main_app/user-settings.html'

    def get_object(self):
        """ Override to get the settings object for the current user. """
        profile = get_object_or_404(Profile, user=self.request.user)
        return get_object_or_404(UserSettings, user=profile)
    
class UserSettingsUpdate(LoginRequiredMixin, TitleMixin, UpdateView):
    model = UserSettings
    title = 'Settings'
    title_color = 'var(--accent-purple)'
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
    title_color = 'var(--accent-yellow)'


class DailyEntryCreate(LoginRequiredMixin, TitleMixin, CreateView):
    title = 'Log'
    title_color = 'var(--accent-yellow)'
    model = DailyEntry
    template_name = 'daily_entries/update.html'
    form_class = DailyEntryForm
    
    def get_initial(self):
        initial = super(DailyEntryCreate, self).get_initial()
        date_str = self.request.GET.get('date', None)
        if date_str:
            initial['date'] = datetime.strptime(date_str, '%Y-%m-%d')
            
        return initial
    
    def get_success_url(self):
        entry_date = self.object.date
        return reverse('daily-entry-read', kwargs={'date': entry_date.strftime('%Y-%m-%d')})
    
    def get_form_kwargs(self):
        kwargs = super(DailyEntryCreate, self).get_form_kwargs()
        profile = Profile.objects.get(user=self.request.user)
        user_settings = UserSettings.objects.filter(user=profile).first()
        kwargs['user_settings'] = user_settings
        return kwargs
    
    def get_context_data(self, **kwargs):
        context = super(DailyEntryCreate, self).get_context_data(**kwargs)
        profile = Profile.objects.get(user=self.request.user)
        context['user_settings'] = UserSettings.objects.filter(user=profile).first()
        context['form_type'] = 'create'  
        return context
    
    def form_valid(self, form):
        profile = get_object_or_404(Profile, user=self.request.user)
        form.instance.user = profile
        self.object = form.save(commit=False)

        emotion_ids = self.request.POST.get('emotion', '')
        if emotion_ids:
            emotion_ids = [int(e_id) for e_id in emotion_ids.split(',') if e_id.isdigit()]
            self.object.save()
            for e_id in emotion_ids:
                emotion = get_object_or_404(Emotion, id=e_id)
                self.object.emotion.add(emotion)
        else:
            self.object.save()

        return super(DailyEntryCreate, self).form_valid(form)


class DailyEntryRead(LoginRequiredMixin, TitleMixin, DetailView):
    title = 'Log'
    title_color = 'var(--accent-yellow)'
    model = DailyEntry
    template_name = 'daily_entries/detail.html'
    success_url = reverse_lazy('daily_entry_detail')
    
    def get_object(self, queryset=None):
        entry_date = date.fromisoformat(self.kwargs.get('date'))
        try:
            profile = Profile.objects.get(user=self.request.user)
            return DailyEntry.objects.get(date=entry_date, user=profile)
        except DailyEntry.DoesNotExist:
            return None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = Profile.objects.get(user=self.request.user)
        context['user_settings'] = UserSettings.objects.filter(user=profile).first()
        context['entry_date'] = date.fromisoformat(self.kwargs.get('date'))
        return context


class DailyEntryUpdate(LoginRequiredMixin, TitleMixin, UpdateView):
    model = DailyEntry
    title = 'Log'
    title_color = 'var(--accent-yellow)'
    form_class = DailyEntryForm
    template_name = 'daily_entries/update.html'
    
    def get_success_url(self):
        entry_date = self.object.date
        return reverse('daily-entry-read', kwargs={'date': entry_date.strftime('%Y-%m-%d')})

    def get_object(self, queryset=None):
        entry_date = date.fromisoformat(self.kwargs.get('date'))
        profile = Profile.objects.get(user=self.request.user)
        return get_object_or_404(DailyEntry, date=entry_date, user=profile)

    def get_context_data(self, **kwargs):
        context = super(DailyEntryUpdate, self).get_context_data(**kwargs)
        profile = Profile.objects.get(user=self.request.user)
        context['user_settings'] = UserSettings.objects.filter(user=profile).first()
        context['form_type'] = 'update'
        entry_date = date.fromisoformat(self.kwargs.get('date'))
        context['date'] = entry_date
        return context

    def get_form_kwargs(self):
        kwargs = super(DailyEntryUpdate, self).get_form_kwargs()
        profile = Profile.objects.get(user=self.request.user)
        user_settings = UserSettings.objects.filter(user=profile).first()
        kwargs['user_settings'] = user_settings
        return kwargs
    
    def form_valid(self, form):
        self.object = form.save(commit=False)

        # Handle emotions
        emotion_ids = self.request.POST.get('emotion', '')
        if emotion_ids:

            emotion_ids = [int(e_id) for e_id in emotion_ids.split(',') if e_id.isdigit()]
            for e_id in emotion_ids:
                emotion = get_object_or_404(Emotion, id=e_id)
                self.object.emotion.add(emotion)

        self.object.save()

        return super(DailyEntryUpdate, self).form_valid(form)


class DailyEntryDelete(LoginRequiredMixin, DeleteView):
    model = DailyEntry
    template_name = 'daily_entries/delete-confirmation.html'
    success_url = '/'
    
    def get_object(self, queryset=None):
        entry_date = date.fromisoformat(self.kwargs.get('date'))
        profile = Profile.objects.get(user=self.request.user)
        return get_object_or_404(DailyEntry, date=entry_date, user=profile)

# Journal Views
class JournalEntryList(LoginRequiredMixin, TitleMixin, ListView):
    model = DailyEntry
    template_name = 'main_app/journal-entries-list.html' 
    title = 'Journals'
    title_color = 'var(--accent-green)'
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
            'id': emotion.id,
            'name': emotion.name,
            'color': emotion.color,
            'timeline_color': emotion.timeline_color,
            'children': [self.get_emotion_data(child) for child in Emotion.objects.filter(parent=emotion.id)]
        }
        return data
    
# Emotions Views
def emotion_lifestyle_timeline(request):
    profile = Profile.objects.get(user=request.user)
    daily_entries = DailyEntry.objects.filter(user=profile)
    user_settings = UserSettings.objects.filter(user=profile).first()

    if not user_settings:
            return JsonResponse({'error': 'User settings not found'}, status=404)

    timeline_data = []

    for entry in daily_entries:
        entry_data = {
            'date': entry.date,
            'emotions': list(entry.emotion.values('name', 'color', 'timeline_color')),
            'lifestyle': {}
        }

        # Check each setting and add to entry_data if it's being tracked
        if user_settings.track_sleep:
            entry_data['lifestyle']['sleep_quality_rating'] = entry.sleep_quality_rating
        if user_settings.track_stress:
            entry_data['lifestyle']['stress_rating'] = entry.stress_rating
        if user_settings.track_physical_health:
            entry_data['lifestyle']['physical_health_rating'] = entry.physical_health_rating
        if user_settings.track_meds:
            entry_data['lifestyle']['has_taken_meds'] = entry.has_taken_meds
        if user_settings.track_sunshine:
            entry_data['lifestyle']['has_gotten_sunshine'] = entry.has_gotten_sunshine
        if user_settings.track_eating_healthily:
            entry_data['lifestyle']['has_eaten_healthily'] = entry.has_eaten_healthily
        if user_settings.track_connecting_socially:
            entry_data['lifestyle']['has_connected_socially'] = entry.has_connected_socially
        if user_settings.track_exercise:
            entry_data['lifestyle']['has_exercised'] = entry.has_exercised
        if user_settings.track_substances:
            entry_data['lifestyle']['has_used_substances'] = entry.has_used_substances
        if user_settings.track_hydrated:
            entry_data['lifestyle']['has_properly_hydrated'] = entry.has_properly_hydrated
        if user_settings.track_menstruation:
            entry_data['lifestyle']['has_menstruated'] = entry.has_menstruated
        if user_settings.track_counseling:
            entry_data['lifestyle']['has_had_counseling'] = entry.has_had_counseling
        if user_settings.track_spirituality:
            entry_data['lifestyle']['has_engaged_spiritually'] = entry.has_engaged_spiritually

        timeline_data.append(entry_data)

    return JsonResponse(timeline_data, safe=False)

def gpt_analysis_view(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            response_text = send_gpt_json(data['timelineData'])  # Make sure this key matches your JS
            return JsonResponse({'response': response_text})
        except json.JSONDecodeError as e:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        except KeyError as e:
            return JsonResponse({'error': 'Missing timelineData key'}, status=400)
        except Exception as e:
            logging.exception("An error occurred: ")
            return JsonResponse({'error': 'Internal Server Error'}, status=500)
    else:
        return JsonResponse({'error': 'Invalid request'}, status=400)