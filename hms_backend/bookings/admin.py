from django.contrib import admin
from .models import Booking

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('patient', 'doctor', 'availability_slot', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('patient__email', 'doctor__email')
    readonly_fields = ('created_at', 'updated_at')
