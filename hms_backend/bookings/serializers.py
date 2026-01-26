from rest_framework import serializers
from .models import Booking
from availability.serializers import DoctorAvailabilitySerializer

class BookingSerializer(serializers.ModelSerializer):
    patient_name = serializers.CharField(source='patient.get_full_name', read_only=True)
    doctor_name = serializers.CharField(source='doctor.get_full_name', read_only=True)
    slot_details = DoctorAvailabilitySerializer(source='availability_slot', read_only=True)
    
    class Meta:
        model = Booking
        fields = ['id', 'patient', 'patient_name', 'doctor', 'doctor_name', 'availability_slot', 'slot_details', 'status', 'notes', 'google_event_id', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at', 'google_event_id']
