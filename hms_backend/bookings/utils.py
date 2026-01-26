import requests
from django.conf import settings

def send_booking_confirmation_email(booking):
    """Send booking confirmation email via serverless function"""
    email_service_url = settings.EMAIL_SERVICE_URL
    
    payload = {
        'action': 'BOOKING_CONFIRMATION',
        'patient_email': booking.patient.email,
        'patient_name': booking.patient.get_full_name(),
        'doctor_name': booking.doctor.get_full_name(),
        'date': str(booking.availability_slot.date),
        'start_time': str(booking.availability_slot.start_time),
        'end_time': str(booking.availability_slot.end_time),
    }
    
    try:
        response = requests.post(
            f'{email_service_url}/send-email',
            json=payload,
            timeout=10
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        raise Exception(f"Failed to send confirmation email: {str(e)}")


def send_booking_cancellation_email(booking):
    """Send booking cancellation email via serverless function"""
    email_service_url = settings.EMAIL_SERVICE_URL
    
    payload = {
        'action': 'BOOKING_CANCELLATION',
        'patient_email': booking.patient.email,
        'patient_name': booking.patient.get_full_name(),
        'doctor_name': booking.doctor.get_full_name(),
        'date': str(booking.availability_slot.date),
        'start_time': str(booking.availability_slot.start_time),
        'end_time': str(booking.availability_slot.end_time),
    }
    
    try:
        response = requests.post(
            f'{email_service_url}/send-email',
            json=payload,
            timeout=10
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        raise Exception(f"Failed to send cancellation email: {str(e)}")
