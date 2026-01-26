from django.urls import path
from . import views

urlpatterns = [
    path('google/auth-url/', views.google_oauth_url, name='google_oauth_url'),
    path('google/callback/', views.google_oauth_callback, name='google_oauth_callback'),
    path('google/check/', views.check_google_connection, name='check_google_connection'),
    path('google/disconnect/', views.disconnect_google, name='disconnect_google'),
]
