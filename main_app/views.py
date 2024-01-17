from django.shortcuts import render

# Create your views here.
def sandbox(request):
    return render(request, 'sandbox.html')