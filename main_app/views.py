from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from .forms import SignUpForm
from .models import UserSettings, DailyEntry
from django.urls import reverse_lazy


# Create your views here.
def home(request):
    return render(request, "home.html")


def sandbox(request):
    return render(request, "sandbox.html")


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
    template_name = 'daily_entries/detail.html'
    success_url = reverse_lazy('daily_entry_detail')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_settings'] = UserSettings.objects.filter(user_id=self.request.user.id).first()
        return context


class DailyEntryUpdate(UpdateView):
    model = DailyEntry


class DailyEntryDelete(DeleteView):
    model = DailyEntry
    success_url = '/daily-entries'

