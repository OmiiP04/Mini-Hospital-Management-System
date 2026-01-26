from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_booking, name='create_booking'),
    path('my-bookings/', views.list_my_bookings, name='list_my_bookings'),
    path('<int:booking_id>/', views.get_booking, name='get_booking'),
    path('<int:booking_id>/cancel/', views.cancel_booking, name='cancel_booking'),
    path('doctor/<int:doctor_id>/', views.get_doctor_bookings, name='get_doctor_bookings'),
]
