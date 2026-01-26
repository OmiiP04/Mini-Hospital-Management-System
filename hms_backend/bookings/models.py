from django.db import models
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from availability.models import DoctorAvailability

User = get_user_model()

class Booking(models.Model):
    STATUS_CHOICES = (
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
    )
    
    patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings_as_patient', limit_choices_to={'role': 'patient'})
    doctor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings_as_doctor', limit_choices_to={'role': 'doctor'})
    availability_slot = models.OneToOneField(DoctorAvailability, on_delete=models.CASCADE, related_name='booking')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='confirmed')
    notes = models.TextField(blank=True, null=True)
    google_event_id = models.CharField(max_length=500, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Booking: {self.patient.get_full_name()} with Dr. {self.doctor.get_full_name()} on {self.availability_slot.date}"
    
    def clean(self):
        # Verify the slot belongs to the doctor
        if self.availability_slot.doctor != self.doctor:
            raise ValidationError("The availability slot must belong to the selected doctor")
        
        # Verify slot is not already booked
        if self.availability_slot.is_booked and not self.pk:
            raise ValidationError("This time slot is already booked")
    
    def save(self, *args, **kwargs):
        self.clean()
        # Mark the slot as booked
        self.availability_slot.book()
        super().save(*args, **kwargs)
    
    def cancel(self):
        """Cancel the booking and free up the slot"""
        self.status = 'cancelled'
        self.availability_slot.is_booked = False
        self.availability_slot.save()
        self.save()
