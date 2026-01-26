# Hospital Management System (HMS)

A comprehensive hospital management web application for managing doctor availability and patient appointment booking with integrated email notifications and Google Calendar sync.

## Technology Stack

- **Backend**: Django 4.2.7
- **Database**: PostgreSQL
- **ORM**: Django ORM
- **Authentication**: Session-based (Username/Email + Password)
- **Email Service**: AWS Lambda with Serverless Framework
- **Calendar Integration**: Google Calendar API with OAuth2

## Features

### 1. User Authentication
- Separate signup for Doctors and Patients
- Secure password hashing
- Session-based authentication
- Role-based access control

### 2. Doctor Features
- Create and manage availability slots (date & time)
- View their own appointments
- Connect to Google Calendar
- Receive appointment notifications

### 3. Patient Features
- Browse available doctors
- View doctor availability slots
- Book appointments with available slots
- Automatic slot blocking after booking
- Cancel bookings if needed
- Receive confirmation notifications

### 4. Appointment Management
- Race condition handling for simultaneous bookings
- Automatic Google Calendar event creation
- Email notifications for confirmations
- Booking history and status tracking

### 5. Serverless Email Service
- SIGNUP_WELCOME emails
- BOOKING_CONFIRMATION emails
- BOOKING_CANCELLATION emails
- Local testing with serverless-offline

## Project Structure

```
Mini Hospital Management System/
├── hms_backend/              # Django backend
│   ├── hms_project/          # Main Django project
│   │   ├── settings.py       # Django settings
│   │   ├── urls.py           # URL routing
│   │   ├── wsgi.py           # WSGI config
│   │   └── asgi.py           # ASGI config
│   ├── users/                # User authentication app
│   │   ├── models.py         # Custom user model
│   │   ├── views.py          # Auth views
│   │   ├── forms.py          # Auth forms
│   │   └── urls.py           # Auth URLs
│   ├── availability/         # Doctor availability app
│   │   ├── models.py         # Availability model
│   │   ├── views.py          # API views
│   │   └── urls.py           # Availability URLs
│   ├── bookings/             # Booking management app
│   │   ├── models.py         # Booking model
│   │   ├── views.py          # Booking views
│   │   └── urls.py           # Booking URLs
│   ├── calendar_integration/ # Google Calendar integration
│   │   ├── utils.py          # Calendar utilities
│   │   ├── views.py          # OAuth views
│   │   └── urls.py           # Calendar URLs
│   ├── templates/            # HTML templates
│   ├── manage.py             # Django management
│   └── requirements.txt      # Python dependencies
│
└── serverless_email/         # Email service (AWS Lambda)
    ├── handler.py            # Lambda handler
    ├── serverless.yml        # Serverless config
    ├── package.json          # Node dependencies
    └── requirements.txt      # Python dependencies
```

## Installation & Setup

### Prerequisites
- Python 3.9+
- PostgreSQL installed locally
- Node.js and npm (for serverless)
- Google OAuth credentials
- Gmail app password

### Backend Setup

1. **Navigate to backend directory:**
```bash
cd hms_backend
```

2. **Create virtual environment:**
```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Configure PostgreSQL:**
```bash
# Create database
createdb hms_db

# If using default postgres user
# psql -U postgres -c "CREATE DATABASE hms_db;"
```

5. **Configure environment variables:**
```bash
# Copy example file
cp .env.example .env

# Edit .env with your settings:
# - DB credentials
# - Google OAuth credentials
# - Secret key
```

6. **Run migrations:**
```bash
python manage.py makemigrations
python manage.py migrate
```

7. **Create superuser:**
```bash
python manage.py createsuperuser
```

8. **Collect static files:**
```bash
python manage.py collectstatic --noinput
```

9. **Run development server:**
```bash
python manage.py runserver
```

Backend will be available at: `http://localhost:8000`

### Serverless Email Service Setup

1. **Navigate to serverless directory:**
```bash
cd serverless_email
```

2. **Install Node dependencies:**
```bash
npm install
```

3. **Set up environment variables:**
```bash
# Copy example file
cp .env.example .env

# Edit .env with your Gmail credentials:
# GMAIL_USER=your-email@gmail.com
# GMAIL_PASSWORD=your-app-password
```

4. **Install serverless-offline locally:**
```bash
npm install --save-dev serverless-offline
```

5. **Run serverless offline:**
```bash
npm run offline
# or
serverless offline start
```

Email service will be available at: `http://localhost:3000`

## API Endpoints

### User Authentication
- `POST /api/users/api/doctor-signup/` - Register as doctor
- `POST /api/users/api/patient-signup/` - Register as patient
- `POST /api/users/api/login/` - Login
- `POST /api/users/api/logout/` - Logout
- `GET /api/users/api/profile/` - Get user profile
- `PUT /api/users/api/profile/update/` - Update profile

### Availability Management
- `POST /api/availability/create/` - Create availability slot (doctor)
- `GET /api/availability/my-slots/` - List doctor's slots
- `GET /api/availability/available-doctors/` - List available doctors (patient)
- `GET /api/availability/doctor/<id>/` - Get doctor's availability
- `GET /api/availability/<slot_id>/` - Get slot details
- `PUT /api/availability/<slot_id>/` - Update slot (doctor)
- `DELETE /api/availability/<slot_id>/` - Delete slot (doctor)

### Booking Management
- `POST /api/bookings/create/` - Create booking (patient)
- `GET /api/bookings/my-bookings/` - List user's bookings
- `GET /api/bookings/<booking_id>/` - Get booking details
- `POST /api/bookings/<booking_id>/cancel/` - Cancel booking
- `GET /api/bookings/doctor/<id>/` - Get doctor's bookings

### Calendar Integration
- `GET /api/calendar/google/auth-url/` - Get Google OAuth URL
- `GET /api/calendar/google/callback/` - OAuth callback
- `GET /api/calendar/google/check/` - Check connection status
- `POST /api/calendar/google/disconnect/` - Disconnect Google Calendar

## Web Interfaces

- **Doctor Signup**: `http://localhost:8000/api/users/doctor-signup/`
- **Patient Signup**: `http://localhost:8000/api/users/patient-signup/`
- **Login**: `http://localhost:8000/api/users/login/`
- **Profile**: `http://localhost:8000/api/users/profile/`
- **Admin Panel**: `http://localhost:8000/admin/`

## Google Calendar Setup

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project
3. Enable Google Calendar API
4. Create OAuth 2.0 credentials (Desktop app)
5. Download credentials as JSON
6. Add credentials to `.env`:
   ```
   GOOGLE_CLIENT_ID=your-client-id
   GOOGLE_CLIENT_SECRET=your-client-secret
   GOOGLE_CALLBACK_URL=http://localhost:8000/api/calendar/google/callback/
   ```

## Gmail Setup for Email Service

1. Enable 2-Step Verification on your Google account
2. Generate an [App Password](https://myaccount.google.com/apppasswords)
3. Add to serverless `.env`:
   ```
   GMAIL_USER=your-email@gmail.com
   GMAIL_PASSWORD=your-16-char-app-password
   ```

## Database Schema

### Users (CustomUser)
- id, username, email, password
- first_name, last_name
- role (doctor/patient)
- phone_number
- google_access_token, google_refresh_token
- created_at, updated_at

### DoctorAvailability
- id, doctor_id, date, start_time, end_time
- is_booked
- created_at, updated_at

### Booking
- id, patient_id, doctor_id, availability_slot_id
- status (confirmed/cancelled/completed)
- notes, google_event_id
- created_at, updated_at

## Usage Example

### Doctor Flow
1. Sign up as doctor
2. Log in to dashboard
3. Create availability slots (e.g., "2024-02-15, 10:00-11:00")
4. Connect Google Calendar (optional)
5. View incoming bookings
6. Receive email notifications

### Patient Flow
1. Sign up as patient
2. Log in to dashboard
3. Browse available doctors and their slots
4. Select a doctor and time slot
5. Book appointment (if slot available)
6. Receive confirmation email
7. Event added to Google Calendar (if connected)
8. Can cancel anytime to free up the slot

## Testing

### Manual Testing

1. **Test Doctor Signup:**
   - Navigate to doctor signup page
   - Fill form with valid data
   - Verify email uniqueness

2. **Test Availability:**
   - Login as doctor
   - Create multiple availability slots
   - Verify slots appear in patient view

3. **Test Booking:**
   - Login as patient
   - Browse available doctors
   - Book a slot
   - Verify slot is blocked

4. **Test Emails:**
   - Check serverless-offline logs
   - Verify email payloads contain correct data

5. **Test Google Calendar:**
   - Connect with Google account
   - Create a booking
   - Check if event appears in Google Calendar

## Demo Video

The 10-minute demo should showcase:
1. Doctor signup and login
2. Creating availability slots
3. Patient signup and login
4. Viewing available doctors
5. Booking an appointment
6. Email notification receipt
7. Google Calendar sync
8. Cancelling a booking
9. Code walkthrough

## Troubleshooting

### PostgreSQL Connection Error
```bash
# Check if PostgreSQL is running
# Windows: Services > PostgreSQL
# macOS: brew services list
# Linux: sudo systemctl status postgresql
```

### Module Not Found
```bash
# Ensure virtual environment is activated
# Reinstall requirements
pip install -r requirements.txt
```

### Email Service Not Responding
```bash
# Verify serverless-offline is running
# Check port 3000 is available
# Verify EMAIL_SERVICE_URL in settings
```

### Google Calendar Error
```bash
# Verify credentials file exists
# Check OAuth URLs are correct
# Ensure tokens are not expired
```

## Production Deployment

### Backend
```bash
# Update settings.py for production
# Configure allowed hosts
# Set DEBUG = False
# Use environment variables for secrets
# Deploy with Gunicorn + Nginx/Apache
```

### Serverless
```bash
# Deploy to AWS Lambda
serverless deploy

# Set environment variables in AWS Lambda console
# Update EMAIL_SERVICE_URL in Django settings
```

## Contributing

1. Create feature branch
2. Make changes
3. Test thoroughly
4. Submit pull request

## License

MIT License

## Support

For issues or questions, create an issue in the repository.

---

**Happy Coding! 🏥**
