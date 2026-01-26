from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.core.exceptions import ValidationError

User = get_user_model()

class DoctorAvailability(models.Model):
    doctor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='availability_slots', limit_choices_to={'role': 'doctor'})
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_booked = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['date', 'start_time']
        unique_together = ('doctor', 'date', 'start_time', 'end_time')
    
    def __str__(self):
        return f"{self.doctor.get_full_name()} - {self.date} {self.start_time}-{self.end_time}"
    
    def clean(self):
        if self.start_time >= self.end_time:
            raise ValidationError("Start time must be before end time")
        
        if timezone.now().date() > self.date:
            raise ValidationError("Cannot create availability for past dates")
    
    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
    
    @property
    def is_available(self):
        """Check if slot is still available (future and not booked)"""
        return not self.is_booked and timezone.now().date() <= self.date
    
    def book(self):
        """Mark slot as booked"""
        if self.is_booked:
            raise ValidationError("This slot is already booked")
        self.is_booked = True
        self.save()
