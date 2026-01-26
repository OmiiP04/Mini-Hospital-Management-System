from django.contrib import admin
from .models import DoctorAvailability

@admin.register(DoctorAvailability)
class DoctorAvailabilityAdmin(admin.ModelAdmin):
    list_display = ('doctor', 'date', 'start_time', 'end_time', 'is_booked', 'created_at')
    list_filter = ('date', 'is_booked', 'created_at')
    search_fields = ('doctor__email', 'doctor__first_name', 'doctor__last_name')
    readonly_fields = ('created_at', 'updated_at')
