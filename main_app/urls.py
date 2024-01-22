from django.urls import path, include, re_path
from . import views

urlpatterns = [
  path('', views.home, name='home'),
  path('sandbox/', views.sandbox, name='sandbox'),
  
  # Auth paths
  path('accounts/', include('django.contrib.auth.urls')),
  path('accounts/signup/', views.signup, name='signup'),
  
  # User Settings URLs
  path('user-settings/', views.UserSettingsUpdate.as_view(), name='user-settings-update'),

  # Daily Entry URLs
  path('daily-entries/', views.DailyEntryList.as_view(), name='daily-entry-list'),
  path('daily-entries/create/', views.DailyEntryCreate.as_view(), name='daily-entry-create'),
  re_path(r'daily-entries/(?P<date>\d{4}-\d{2}-\d{2})/update/', views.DailyEntryUpdate.as_view(), name='daily-entry-update'),
  re_path(r'daily-entries/(?P<date>\d{4}-\d{2}-\d{2})/delete/', views.DailyEntryDelete.as_view(), name='daily-entry-delete'),
  re_path(r'daily-entries/(?P<date>\d{4}-\d{2}-\d{2})/', views.DailyEntryRead.as_view(), name='daily-entry-read'),
  
  # Journal Entry URLs
  path('journal-entries/', views.JournalEntryList.as_view(), name='journal-entries-list'),
  
  # Emotion URLs
  path('api/emotions/', views.EmotionsDataView.as_view(), name='emotions-data'),

  #Timeline URLs
  path('timeline/', views.timeline, name='timeline'),
  path('timeline/lifestyle_view', views.process_lifestyle_selector, name='process_lifestyle_selector'),
]