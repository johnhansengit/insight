from django.urls import path, include
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
  path('daily-entries/<int:pk>/', views.DailyEntryRead.as_view(), name='daily-entry-read'),
  path('daily-entries/<int:pk>/update', views.DailyEntryUpdate.as_view(), name='daily-entry-update'),
  path('daily-entries/<int:pk>/delete', views.DailyEntryDelete.as_view(), name='daily-entry-delete'),
  
  # Journal Entry URLs
  path('journal-entries/', views.JournalEntryList.as_view(), name='journal-entries-list'),
  
  # Emotion URLs
  path('api/emotions/', views.EmotionsDataView.as_view(), name='emotions-data'),

  #Timeline URLs
  path('timeline/', views.timeline, name='timeline'),
]