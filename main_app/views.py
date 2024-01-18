from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import SignUpForm


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
            return redirect("sandbox")
    form = SignUpForm()
    context = {"form": form}
    return render(request, "registration/signup.html", context)
