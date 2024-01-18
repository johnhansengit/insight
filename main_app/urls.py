from django.urls import path, include
from . import views

urlpatterns = [
  path('', views.home, name='home'),
  path('sandbox/', views.sandbox, name='sandbox'),
  
  # Auth paths
  path('accounts/', include('django.contrib.auth.urls')),
  path('accounts/signup/', views.signup, name='signup'),
  
  # User Settings URLs
  path('user-settings/create/', views.UserSettingsCreate.as_view(), name='user-settings-create'),
  path('user-settings/<int:pk>/', views.UserSettingsRead.as_view(), name='user-settings-read'),
  path('user-settings/<int:pk>/update', views.UserSettingsUpdate.as_view(), name='user-settings-update'),

  # Daily Entry URLs
  path('daily-entries/', views.DailyEntryList.as_view(), name='daily-entry-list'),
  path('daily-entries/create/', views.DailyEntryCreate.as_view(), name='daily-entry-create'),
  path('daily-entries/<int:pk>/', views.DailyEntryRead.as_view(), name='daily-entry-read'),
  path('daily-entries/<int:pk>/update', views.DailyEntryUpdate.as_view(), name='daily-entry-update'),
  path('daily-entries/<int:pk>/delete', views.DailyEntryDelete.as_view(), name='daily-entry-delete'),
]