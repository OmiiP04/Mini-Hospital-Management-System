from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_availability, name='create_availability'),
    path('my-slots/', views.list_my_availability, name='list_my_availability'),
    path('available-doctors/', views.list_available_doctors, name='list_available_doctors'),
    path('doctors/', views.list_all_doctors, name='list_all_doctors'),
    path('doctor/<int:doctor_id>/', views.get_doctor_availability, name='get_doctor_availability'),
    path('<int:slot_id>/', views.manage_availability, name='manage_availability'),
]
