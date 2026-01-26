from django.urls import path
from . import views

urlpatterns = [
    # Web views
    path('doctor-signup/', views.doctor_signup, name='doctor_signup'),
    path('patient-signup/', views.patient_signup, name='patient_signup'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('profile/', views.profile, name='profile'),
    
    # API endpoints
    path('api/doctor-signup/', views.api_doctor_signup, name='api_doctor_signup'),
    path('api/patient-signup/', views.api_patient_signup, name='api_patient_signup'),
    path('api/login/', views.api_login, name='api_login'),
    path('api/logout/', views.api_logout, name='api_logout'),
    path('api/profile/', views.api_profile, name='api_profile'),
    path('api/profile/update/', views.api_update_profile, name='api_update_profile'),
]
