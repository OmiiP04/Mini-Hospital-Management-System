"""
URL configuration for hms_project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.http import JsonResponse
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/users/', include('users.urls')),
    path('api/availability/', include('availability.urls')),
    path('api/bookings/', include('bookings.urls')),
    # path('api/calendar/', include('calendar_integration.urls')),
    path('', lambda request: JsonResponse({"message": "Welcome to the Hospital Management System API"}), name='home'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
