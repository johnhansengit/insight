from django.urls import path, include
from . import views

urlpatterns = [
  path('sandbox/', views.sandbox, name='sandbox'),
  
  # Auth paths
  path('accounts/', include('django.contrib.auth.urls')),
]