# HMS Project Requirements Checklist

## Tech Stack
- ✅ **Backend Framework**: Django 4.2.7
- ✅ **Database**: PostgreSQL 
- ✅ **ORM**: Django ORM
- ✅ **Authentication**: Session-based with Username/Email + Password
- ✅ **Serverless Email Service**: AWS Lambda with Serverless Framework

---

## User Roles & Authentication

### ✅ 1. Authentication System
- ✅ Sign up for Doctors
- ✅ Sign up for Patients
- ✅ Login for both roles
- ✅ Password hashing (Django's built-in `make_password`)
- ✅ Role-based access control
  - File: [users/models.py](hms_backend/users/models.py) - CustomUser model with role choices
  - File: [users/views.py](hms_backend/users/views.py) - Signup/login views

### ✅ 2. Doctor Features
- ✅ Can sign up & log in
  - File: [users/models.py](hms_backend/users/models.py#L5) - Role field
  - File: [users/views.py](hms_backend/users/views.py) - Auth views
- ✅ Has a doctor dashboard
  - File: [templates/dashboards/doctor_dashboard.html](hms_backend/templates/dashboards/doctor_dashboard.html)
- ✅ Can set/update availability time slots (date & time)
  - File: [availability/models.py](hms_backend/availability/models.py) - DoctorAvailability model
  - File: [availability/views.py](hms_backend/availability/views.py) - Create/update slots
- ✅ Only see & manage their own availability and bookings
  - File: [availability/views.py](hms_backend/availability/views.py#L15) - Doctor-specific filtering
  - File: [bookings/views.py](hms_backend/bookings/views.py#L62) - `list_my_bookings` with role check

### ✅ 3. Patient Features
- ✅ Can sign up & log in
  - File: [users/views.py](hms_backend/users/views.py)
- ✅ Has a patient dashboard
  - File: [templates/dashboards/patient_dashboard.html](hms_backend/templates/dashboards/patient_dashboard.html)
- ✅ Can view doctors and their available time slots
  - File: [availability/views.py](hms_backend/availability/views.py#L48) - `list_available_slots`
- ✅ Can book one available time slot with a doctor
  - File: [bookings/views.py](hms_backend/bookings/views.py#L12) - `create_booking`
- ✅ Once a slot is booked, it must be blocked so nobody else can book the same slot
  - File: [availability/models.py](hms_backend/availability/models.py#L20) - `is_booked` field
  - File: [bookings/models.py](hms_backend/bookings/models.py#L35) - Automatic slot marking in save()

---

## Core Functional Requirements

### ✅ 1. Authentication
- ✅ Sign up & login for both doctors and patients
  - File: [users/views.py](hms_backend/users/views.py) - signup_doctor, signup_patient, login views
- ✅ Store password securely (hashed)
  - Django's default: `make_password()` uses PBKDF2
- ✅ Role-based access
  - File: [users/models.py](hms_backend/users/models.py#L6) - `is_doctor()` and `is_patient()` methods
  - File: [bookings/views.py](hms_backend/bookings/views.py#L13-L14) - Permission checks

### ✅ 2. Doctor Availability
- ✅ Doctor can create availability slots by date & time
  - File: [availability/models.py](hms_backend/availability/models.py) - DoctorAvailability model
  - File: [availability/views.py](hms_backend/availability/views.py#L12) - `create_availability` view
- ✅ Slots visible to patients only if:
  - ✅ In the future
    - File: [availability/models.py](hms_backend/availability/models.py#L28) - Validation in clean()
    - File: [availability/models.py](hms_backend/availability/models.py#L34) - `is_available` property
  - ✅ Not already booked
    - File: [availability/models.py](hms_backend/availability/models.py#L34) - `is_booked` check

### ✅ 3. Booking Flow
- ✅ Patient selects:
  - ✅ Doctor
  - ✅ Date
  - ✅ Time slot
  - File: [bookings/views.py](hms_backend/bookings/views.py#L17-L20)
- ✅ System:
  - ✅ Verifies slot is still free (avoid race conditions)
    - File: [bookings/views.py](hms_backend/bookings/views.py#L28) - Explicit check
    - File: [bookings/views.py](hms_backend/bookings/views.py#L35) - `transaction.atomic()` for race condition prevention
  - ✅ Creates a booking
    - File: [bookings/views.py](hms_backend/bookings/views.py#L36-L40) - Booking.objects.create()
  - ✅ Marks that slot as booked so others can't take it
    - File: [bookings/models.py](hms_backend/bookings/models.py#L35) - Automatic in save()

### ✅ 4. Google Calendar Integration
- ✅ When a booking is confirmed:
  - ✅ Create calendar event in doctor's Google Calendar
    - File: [calendar_integration/utils.py](hms_backend/calendar_integration/utils.py#L47)
  - ✅ Create calendar event in patient's Google Calendar
    - File: [calendar_integration/utils.py](hms_backend/calendar_integration/utils.py#L74)
- ✅ Assume one Google account per user (doctor/patient)
  - File: [users/models.py](hms_backend/users/models.py#L13-L14) - google_access_token, google_refresh_token fields
- ✅ Use Google Calendar API with OAuth2
  - File: [calendar_integration/utils.py](hms_backend/calendar_integration/utils.py#L13) - SCOPES definition
  - File: [calendar_integration/utils.py](hms_backend/calendar_integration/utils.py#L16) - `get_google_calendar_service()` 
  - File: [calendar_integration/views.py](hms_backend/calendar_integration/views.py) - OAuth views
- ✅ Event details:
  - ✅ Title: "Appointment with Dr. {DoctorName}" / "Appointment with {PatientName}"
    - File: [calendar_integration/utils.py](hms_backend/calendar_integration/utils.py#L56) - Doctor's event
    - File: [calendar_integration/utils.py](hms_backend/calendar_integration/utils.py#L77) - Patient's event
  - ✅ Start & end time = selected slot
    - File: [calendar_integration/utils.py](hms_backend/calendar_integration/utils.py#L60-L66)
  - ✅ Optional description
    - File: [calendar_integration/utils.py](hms_backend/calendar_integration/utils.py#L57)

### ✅ 5. Email Notification via Serverless Function
- ✅ Separate mini-project: Python serverless function on AWS Lambda
  - File: [serverless_email/handler.py](serverless_email/handler.py)
  - File: [serverless_email/serverless.yml](serverless_email/serverless.yml)
- ✅ Using Serverless Framework
  - File: [serverless_email/serverless.yml](serverless_email/serverless.yml)
- ✅ Support for:
  - ✅ SIGNUP_WELCOME – send welcome email on sign up
    - File: [serverless_email/handler.py](serverless_email/handler.py#L27) - `send_welcome_email()`
  - ✅ BOOKING_CONFIRMATION – send confirmation email on booking
    - File: [serverless_email/handler.py](serverless_email/handler.py#L29) - `send_booking_confirmation()`
  - ✅ BOOKING_CANCELLATION – send cancellation email
    - File: [serverless_email/handler.py](serverless_email/handler.py#L31) - `send_booking_cancellation()`
- ✅ HMS backend calls Lambda via HTTP endpoint
  - File: [bookings/utils.py](hms_backend/bookings/utils.py) - Email service caller
  - File: [bookings/views.py](hms_backend/bookings/views.py#L49-L53) - Called from create_booking
- ✅ Can be tested using serverless-offline
  - File: [serverless_email/local_test.py](serverless_email/local_test.py) - Local test server
  - File: [serverless_email/serverless.yml](serverless_email/serverless.yml) - serverless-offline config

### ✅ 6. Offline / Local Demo
- ✅ Run the main app locally (Django)
  ```bash
  cd hms_backend
  python manage.py runserver
  ```
  - File: [hms_backend/manage.py](hms_backend/manage.py)
  - File: [SETUP_AND_TESTING.md](SETUP_AND_TESTING.md) - Setup instructions
- ✅ Run serverless email service using serverless offline
  ```bash
  cd serverless_email
  python local_test.py
  ```
  - File: [serverless_email/local_test.py](serverless_email/local_test.py)
  - File: [serverless_email/serverless.yml](serverless_email/serverless.yml)

---

## Summary

✅ **ALL REQUIREMENTS SATISFIED**

### Completed Features:
1. ✅ Full user authentication (Doctors & Patients)
2. ✅ Doctor availability management
3. ✅ Patient booking system with race condition handling
4. ✅ Google Calendar integration with OAuth2
5. ✅ Serverless email notifications (3 email types)
6. ✅ Local development environment
7. ✅ Role-based access control
8. ✅ Secure password hashing
9. ✅ Automatic slot blocking after booking
10. ✅ Email service testing with Postman ✅ (Just completed!)

### Files Summary:
- **Backend Models**: 5 apps (users, availability, bookings, calendar_integration, hms_project)
- **Frontend**: HTML templates for both doctor & patient dashboards
- **Serverless**: AWS Lambda function with 3 email templates
- **Configuration**: Django settings, Serverless config, requirements.txt

### Next Steps:
1. Deploy to AWS Lambda: `serverless deploy`
2. Configure PostgreSQL for production
3. Set up Google OAuth credentials
4. Deploy Django backend to a web server
5. Configure custom domain and SSL certificates
