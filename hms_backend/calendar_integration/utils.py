from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from google.auth.oauthlib.flow import Flow
from googleapiclient.discovery import build
from django.conf import settings
from django.contrib.auth import get_user_model
import json

User = get_user_model()

# Google Calendar API Scope
SCOPES = ['https://www.googleapis.com/auth/calendar']

def get_google_calendar_service(user):
    """Get Google Calendar service for a user"""
    if not user.google_access_token:
        return None
    
    credentials = Credentials(
        token=user.google_access_token,
        refresh_token=user.google_refresh_token,
        token_uri='https://oauth2.googleapis.com/token',
        client_id=settings.GOOGLE_CLIENT_ID,
        client_secret=settings.GOOGLE_CLIENT_SECRET
    )
    
    # Refresh if needed
    if credentials.expired and credentials.refresh_token:
        try:
            credentials.refresh(Request())
            # Save new tokens
            user.google_access_token = credentials.token
            user.google_refresh_token = credentials.refresh_token
            user.save()
        except Exception as e:
            print(f"Token refresh failed: {str(e)}")
            return None
    
    return build('calendar', 'v3', credentials=credentials)


def create_calendar_event(booking):
    """Create calendar events for both doctor and patient"""
    doctor = booking.doctor
    patient = booking.patient
    slot = booking.availability_slot
    
    event_id = None
    
    # Create event for doctor
    if doctor.google_access_token:
        try:
            service = get_google_calendar_service(doctor)
            if service:
                event_body = {
                    'summary': f'Appointment with {patient.get_full_name()}',
                    'description': f'Patient: {patient.get_full_name()}\nEmail: {patient.email}\nPhone: {patient.phone_number}',
                    'start': {
                        'dateTime': f'{slot.date}T{slot.start_time}:00',
                        'timeZone': 'UTC',
                    },
                    'end': {
                        'dateTime': f'{slot.date}T{slot.end_time}:00',
                        'timeZone': 'UTC',
                    },
                }
                
                event = service.events().insert(calendarId='primary', body=event_body).execute()
                event_id = event.get('id')
        except Exception as e:
            print(f"Failed to create doctor's calendar event: {str(e)}")
    
    # Create event for patient
    if patient.google_access_token:
        try:
            service = get_google_calendar_service(patient)
            if service:
                event_body = {
                    'summary': f'Appointment with Dr. {doctor.get_full_name()}',
                    'description': f'Doctor: {doctor.get_full_name()}\nEmail: {doctor.email}\nPhone: {doctor.phone_number}',
                    'start': {
                        'dateTime': f'{slot.date}T{slot.start_time}:00',
                        'timeZone': 'UTC',
                    },
                    'end': {
                        'dateTime': f'{slot.date}T{slot.end_time}:00',
                        'timeZone': 'UTC',
                    },
                }
                
                event = service.events().insert(calendarId='primary', body=event_body).execute()
                if not event_id:
                    event_id = event.get('id')
        except Exception as e:
            print(f"Failed to create patient's calendar event: {str(e)}")
    
    return event_id


def delete_calendar_event(booking):
    """Delete calendar event when booking is cancelled"""
    doctor = booking.doctor
    patient = booking.patient
    event_id = booking.google_event_id
    
    if not event_id:
        return
    
    # Delete from doctor's calendar
    if doctor.google_access_token:
        try:
            service = get_google_calendar_service(doctor)
            if service:
                service.events().delete(calendarId='primary', eventId=event_id).execute()
        except Exception as e:
            print(f"Failed to delete doctor's calendar event: {str(e)}")
    
    # Delete from patient's calendar
    if patient.google_access_token:
        try:
            service = get_google_calendar_service(patient)
            if service:
                service.events().delete(calendarId='primary', eventId=event_id).execute()
        except Exception as e:
            print(f"Failed to delete patient's calendar event: {str(e)}")


def get_auth_url():
    """Get Google OAuth authorization URL"""
    flow = Flow.from_client_secrets_file(
        'client_secrets.json',
        scopes=SCOPES
    )
    flow.redirect_uri = settings.GOOGLE_CALLBACK_URL
    
    auth_url, state = flow.authorization_url(access_type='offline', prompt='consent')
    return auth_url, state


def handle_oauth_callback(code, state):
    """Handle OAuth callback and save tokens"""
    flow = Flow.from_client_secrets_file(
        'client_secrets.json',
        scopes=SCOPES,
        state=state
    )
    flow.redirect_uri = settings.GOOGLE_CALLBACK_URL
    
    credentials = flow.fetch_token(code=code)
    
    return {
        'access_token': credentials.get('access_token'),
        'refresh_token': credentials.get('refresh_token'),
    }
