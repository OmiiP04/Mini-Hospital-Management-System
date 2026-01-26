from rest_framework import serializers
from .models import DoctorAvailability
from users.serializers import UserSerializer

class DoctorAvailabilitySerializer(serializers.ModelSerializer):
    doctor_name = serializers.CharField(source='doctor.get_full_name', read_only=True)
    is_available = serializers.SerializerMethodField()
    
    class Meta:
        model = DoctorAvailability
        fields = ['id', 'doctor', 'doctor_name', 'date', 'start_time', 'end_time', 'is_booked', 'is_available', 'created_at']
        read_only_fields = ['id', 'created_at', 'is_booked']
    
    def get_is_available(self, obj):
        return obj.is_available
