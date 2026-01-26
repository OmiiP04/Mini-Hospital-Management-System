# Hospital Management System - COMPLETE SETUP & TESTING GUIDE

## 📋 Table of Contents
1. [Prerequisites](#prerequisites)
2. [Full Installation](#full-installation)
3. [Configuration](#configuration)
4. [Running the System](#running-the-system)
5. [Testing Guide](#testing-guide)
6. [Demo Walkthrough](#demo-walkthrough)
7. [Troubleshooting](#troubleshooting)

---

## Prerequisites

### System Requirements
- **OS**: Windows, macOS, or Linux
- **Python**: 3.9 or higher
- **PostgreSQL**: 12 or higher
- **Node.js**: 14 or higher
- **npm**: 6 or higher
- **Git**: For version control

### Verify Installation
```bash
# Check Python
python --version

# Check PostgreSQL
psql --version

# Check Node.js
node --version
npm --version
```

---

## Full Installation

### Step 1: Database Setup

#### Windows (PostgreSQL)
1. Download from https://www.postgresql.org/download/windows/
2. Run installer
3. Note username (default: postgres) and password
4. Create database:
```bash
psql -U postgres -c "CREATE DATABASE hms_db;"
```

#### macOS
```bash
# Using Homebrew
brew install postgresql@14
brew services start postgresql@14

# Create database
createdb hms_db
```

#### Linux (Ubuntu/Debian)
```bash
# Install PostgreSQL
sudo apt-get update
sudo apt-get install postgresql postgresql-contrib

# Create database
sudo -u postgres createdb hms_db
```

**Verify**: `psql hms_db` (should connect)

---

### Step 2: Backend Installation

#### 2.1 Navigate to Backend Directory
```bash
cd hms_backend
```

#### 2.2 Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

#### 2.3 Install Dependencies
```bash
pip install -r requirements.txt
```

**Expected packages**:
- Django 4.2.7
- djangorestframework 3.14.0
- psycopg2-binary 2.9.9
- google-auth-oauthlib 1.2.0
- requests 2.31.0

#### 2.4 Environment Configuration
```bash
# Copy example file
cp .env.example .env

# Edit .env file with your settings
# Windows: notepad .env
# macOS/Linux: nano .env
```

**Configure these values**:
```env
DEBUG=True
SECRET_KEY=django-insecure-change-this-in-production
DB_ENGINE=django.db.backends.postgresql
DB_NAME=hms_db
DB_USER=postgres              # Your PostgreSQL user
DB_PASSWORD=your_password     # Your PostgreSQL password
DB_HOST=localhost
DB_PORT=5432
```

#### 2.5 Run Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

**Expected output**:
```
Applying users.0001_initial... OK
Applying availability.0001_initial... OK
Applying bookings.0001_initial... OK
...
```

#### 2.6 Create Superuser
```bash
python manage.py createsuperuser
```

**Example**:
```
Username: admin
Email: admin@example.com
Password: AdminPass123
Password (again): AdminPass123
```

#### 2.7 Collect Static Files
```bash
python manage.py collectstatic --noinput
```

---

### Step 3: Serverless Email Service Installation

#### 3.1 Navigate to Serverless Directory
```bash
cd ../serverless_email
```

#### 3.2 Install Node Dependencies
```bash
npm install
```

**Expected packages**:
- serverless ^3.26.0
- serverless-offline ^12.0.4
- serverless-python-requirements ^6.0.0

#### 3.3 Gmail Setup

1. Go to https://myaccount.google.com/
2. Select "Security" from left menu
3. Enable 2-Step Verification if not done
4. Go to "App passwords" (under 2-Step Verification)
5. Select "Mail" and "Windows Computer" (or your device)
6. Copy the 16-character password

#### 3.4 Environment Configuration
```bash
# Copy example file
cp .env.example .env

# Edit .env
# Windows: notepad .env
# macOS/Linux: nano .env
```

**Configure these values**:
```env
GMAIL_USER=your-email@gmail.com
GMAIL_PASSWORD=xxxx-xxxx-xxxx-xxxx  # 16-char app password
```

---

## Configuration

### Google Calendar Setup (Optional)

#### 1. Create Google Cloud Project
1. Go to https://console.cloud.google.com/
2. Click "Select a project" → "New Project"
3. Name it "HMS"
4. Click "Create"

#### 2. Enable Google Calendar API
1. Search for "Google Calendar API"
2. Click "Enable"

#### 3. Create OAuth Credentials
1. Go to "Credentials" in left menu
2. Click "Create Credentials" → "OAuth 2.0 Client IDs"
3. Choose "Desktop application"
4. Download JSON file
5. Save credentials:
   - GOOGLE_CLIENT_ID
   - GOOGLE_CLIENT_SECRET

#### 4. Update Backend Configuration
```bash
# Edit hms_backend/.env
GOOGLE_CLIENT_ID=your-client-id.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=your-client-secret
```

---

## Running the System

### Terminal 1: Start PostgreSQL

#### Windows
```bash
# PostgreSQL service should auto-start
# If not: Services > PostgreSQL > Start
```

#### macOS
```bash
brew services start postgresql@14
```

#### Linux
```bash
sudo systemctl start postgresql
```

**Verify**: `psql hms_db` (should connect)

---

### Terminal 2: Start Django Backend

```bash
cd hms_backend
source venv/bin/activate          # Windows: venv\Scripts\activate
python manage.py runserver
```

**Expected output**:
```
Watching for file changes with StatReloader
Performing system checks...

System check identified no issues (0 silenced).
Django version 4.2.7, using settings 'hms_project.settings'
Starting development server at http://127.0.0.1:8000/
```

**Access**:
- Website: http://localhost:8000
- Admin: http://localhost:8000/admin/

---

### Terminal 3: Start Serverless Email Service

```bash
cd serverless_email
npm run offline
```

**Expected output**:
```
Starting Serverless offline v12.0.4 ...

Starting service offline listening on port 3000
```

**Access**:
- Email service: http://localhost:3000/send-email

---

## Testing Guide

### Phase 1: Basic Setup Verification

#### Test 1.1: Django Server
```
✓ Visit http://localhost:8000
✓ Should see login page
✓ Visit http://localhost:8000/admin
✓ Should see admin login
```

#### Test 1.2: Database Connection
```bash
# In Django shell
python manage.py shell
>>> from django.contrib.auth import get_user_model
>>> User = get_user_model()
>>> print(User.objects.count())
0  # Should be 0 initially
```

#### Test 1.3: Admin Access
```
✓ Go to http://localhost:8000/admin/
✓ Login with superuser credentials
✓ Should see Users, Availability, Bookings sections
```

---

### Phase 2: User Registration & Authentication

#### Test 2.1: Doctor Signup
1. Go to http://localhost:8000/api/users/doctor-signup/
2. Fill form:
   - First Name: John
   - Last Name: Doe
   - Email: doctor1@example.com
   - Phone: 555-0001
   - Password: DoctorPass123
   - Confirm: DoctorPass123
3. Click "Create Doctor Account"
4. **Expected**: Redirect to login page with success message

#### Test 2.2: Patient Signup
1. Go to http://localhost:8000/api/users/patient-signup/
2. Fill form:
   - First Name: Jane
   - Last Name: Smith
   - Email: patient1@example.com
   - Phone: 555-0002
   - Password: PatientPass123
   - Confirm: PatientPass123
3. Click "Create Patient Account"
4. **Expected**: Redirect to login page with success message

#### Test 2.3: Doctor Login
1. Go to http://localhost:8000/api/users/login/
2. Enter:
   - Email/Username: doctor1@example.com
   - Password: DoctorPass123
3. Click "Login"
4. **Expected**: Redirect to dashboard with welcome message

#### Test 2.4: Patient Login
1. Go to http://localhost:8000/api/users/login/
2. Enter:
   - Email/Username: patient1@example.com
   - Password: PatientPass123
3. Click "Login"
4. **Expected**: Redirect to dashboard with welcome message

---

### Phase 3: Doctor Availability Management

#### Test 3.1: Create Availability Slot
**Login as doctor**
1. In Doctor Dashboard, fill:
   - Date: 2024-02-15
   - Start Time: 10:00
   - End Time: 11:00
2. Click "Create Slot"
3. **Expected**: Slot appears in table

#### Test 3.2: Create Multiple Slots
```
Slot 1: 2024-02-15, 10:00-11:00
Slot 2: 2024-02-15, 14:00-15:00
Slot 3: 2024-02-16, 09:00-10:00
```

#### Test 3.3: View Slots
- Doctor Dashboard should show all slots
- Check badge shows "Available"
- Verify dates are in the future

#### Test 3.4: Edit Slot
1. Click "Edit" on an available slot
2. Change time to 11:30
3. Save
4. **Expected**: Slot updated with new time

#### Test 3.5: Cannot Edit Booked Slot
1. (After patient books) Click "Edit" on booked slot
2. **Expected**: Button disabled or error message

---

### Phase 4: Patient Booking

#### Test 4.1: View Available Doctors
**Login as patient**
1. Go to "Find Doctor" section
2. **Expected**: 
   - See doctor cards
   - Each shows available slots
   - Inline slot display

#### Test 4.2: Book Appointment
1. Click on doctor card
2. Modal opens showing slots
3. Select slot: "2024-02-15 10:00-11:00"
4. Add notes: "Regular checkup"
5. Click "Confirm Booking"
6. **Expected**:
   - Booking appears in "My Bookings"
   - Slot shows as "Booked" in doctor view

#### Test 4.3: Verify Slot Blocking
**Login as doctor (new browser/incognito)**
1. View availability
2. Previously booked slot should show "Booked"
3. Cannot be booked again

#### Test 4.4: Cannot Double Book
**In same browser, different patient login**
1. Try to book same slot again
2. **Expected**: Error "Slot already booked"

#### Test 4.5: View My Bookings
**As patient**
1. Go to "My Bookings" section
2. **Expected**:
   - Shows doctor name
   - Shows date and time
   - Shows status "Confirmed"
   - Shows "Cancel" button

---

### Phase 5: Email Notifications

#### Test 5.1: Check Serverless Logs
```bash
# In serverless terminal
# Look for POST /send-email requests
# Should see logs when creating bookings
```

#### Test 5.2: Manual Email Test
```bash
# In hms_backend directory
python manage.py shell

from bookings.utils import send_booking_confirmation_email
# Check serverless terminal for request

# To monitor in real-time:
# 1. Keep serverless offline running
# 2. Create booking in browser
# 3. Check serverless logs
```

#### Test 5.3: Email Contents
Serverless should log requests containing:
- action: "BOOKING_CONFIRMATION"
- patient_email
- doctor_name
- date, start_time, end_time

---

### Phase 6: Booking Cancellation

#### Test 6.1: Cancel Booking
**As patient**
1. Go to "My Bookings"
2. Click "Cancel" on confirmed booking
3. Confirm cancellation
4. **Expected**:
   - Status changes to "Cancelled"
   - Cannot book that slot anymore (error)

#### Test 6.2: Verify Slot Released
**As doctor**
1. View availability
2. Previously booked slot should now show "Available"

#### Test 6.3: Rebook Released Slot
**As different patient**
1. Should be able to book the freed slot
2. **Expected**: Booking succeeds

---

### Phase 7: Google Calendar Integration

#### Test 7.1: Connect Google Calendar
**Login as doctor**
1. Click "Connect Google Calendar"
2. Authorize with your Google account
3. Allow calendar access
4. **Expected**: Shows "Connected" status

#### Test 7.2: Event on Booking
**With Google connected**
1. Create a booking (as patient with doctor having Google connected)
2. Check Google Calendar
3. **Expected**:
   - Event appears in doctor's calendar
   - Event appears in patient's calendar
   - Title shows doctor/patient name
   - Time matches appointment

#### Test 7.3: Event Deletion
1. Cancel booking
2. Check Google Calendar
3. **Expected**: Event disappears

---

## Demo Walkthrough

### 10-Minute Demonstration Script

#### Setup (30 seconds)
```
"Welcome to the Hospital Management System. Let me show you the complete 
system for managing doctor appointments online."

Show terminal windows running:
- Django backend (port 8000)
- Serverless email (port 3000)
- PostgreSQL running
```

#### Part 1: Signup (1 minute)
```
"First, let's create accounts. I'll sign up as a doctor."

1. Go to http://localhost:8000/api/users/doctor-signup/
2. Fill form with:
   - Name: Dr. John Smith
   - Email: doctor@example.com
   - Password: Test123456
3. Submit → Success message

"Now as a patient."

1. Go to http://localhost:8000/api/users/patient-signup/
2. Fill form with:
   - Name: Jane Doe
   - Email: patient@example.com
   - Password: Test123456
3. Submit → Success message

"Both have accounts. Let me check the database."

Show admin interface with both users.
```

#### Part 2: Doctor Features (2 minutes)
```
"Now let's create some availability slots as a doctor."

1. Login as doctor
2. Show doctor dashboard
3. Create availability:
   - 2024-02-15, 10:00-11:00
   - 2024-02-15, 14:00-15:00
   - 2024-02-16, 09:00-10:00

"The system validates that slots are in the future and prevents double-booking."

Show stats:
- Total Availability Slots: 3
- Available Slots: 3
- Booked Appointments: 0

"Let me show the code that validates this..."

Open models.py, show DoctorAvailability.clean() method.
```

#### Part 3: Patient Booking (2 minutes)
```
"Now let's book an appointment as a patient."

1. Login as patient
2. Show patient dashboard
3. Browse available doctors
   - Click to expand slots
   - Show time options
4. Select doctor
5. Show booking modal
6. Select time slot
7. Add notes
8. Confirm booking

"The system uses atomic transactions to prevent race conditions..."

Show bookings/views.py, highlight @transaction.atomic()

"And immediately blocks the slot from other patients."

Show doctor's availability - slot now shows "Booked"

"The patient receives a confirmation email..."

Show serverless terminal logs with POST request.
```

#### Part 4: Google Calendar (2 minutes)
```
"The system also integrates with Google Calendar."

1. Show "Connect Google Calendar" button in doctor dashboard
2. Login with Google
3. Authorize access
4. Show "Connected" status

"When we made that booking, the system automatically created events 
in both the doctor's and patient's Google Calendar."

Show browser with Google Calendar open in another tab.
- Event visible in both calendars
- Title shows appointment details

"If we cancel the appointment..."

1. Show cancellation in patient dashboard
2. Automatic email sent
3. Event automatically deleted from Google Calendar
```

#### Part 5: Code Walkthrough (2 minutes)
```
"Let me show you some key code pieces."

1. Show Models (models.py files)
   - CustomUser with roles
   - DoctorAvailability with validation
   - Booking with OneToOne to DoctorAvailability
   - Race condition handling

2. Show Booking Logic (bookings/views.py)
   - Atomic transaction
   - Slot verification
   - Calendar event creation
   - Email notification

3. Show Email Integration (bookings/utils.py)
   - Calls serverless function
   - Passes appointment details

4. Show Calendar Sync (calendar_integration/utils.py)
   - OAuth2 token handling
   - Event creation/deletion
   - Error handling
```

#### Conclusion (30 seconds)
```
"This system demonstrates:
- User authentication with roles
- Database integrity with transactions
- Third-party API integration (Google Calendar)
- Serverless functions for notifications
- Responsive web interface

The complete source code is well-documented and production-ready."
```

---

## Troubleshooting

### Database Issues

#### "psql: could not connect to server"
```bash
# Start PostgreSQL service
# Windows: Services > PostgreSQL > Start
# macOS: brew services start postgresql@14
# Linux: sudo systemctl start postgresql

# Verify:
psql -U postgres
```

#### "FATAL: database 'hms_db' does not exist"
```bash
# Create database
createdb hms_db
# or
psql -U postgres -c "CREATE DATABASE hms_db;"
```

#### "FATAL: authentication failed for user 'postgres'"
```bash
# Edit .env with correct credentials
# Default PostgreSQL user: postgres
# Check DB_PASSWORD in .env
```

---

### Django Issues

#### "ModuleNotFoundError: No module named 'django'"
```bash
# Ensure virtual environment is activated
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate      # Windows

# Reinstall requirements
pip install -r requirements.txt
```

#### "No such table: users_customuser"
```bash
# Run migrations
python manage.py migrate
```

#### "Port 8000 already in use"
```bash
# Use different port
python manage.py runserver 8001

# Or kill process using port 8000
# Windows: netstat -ano | findstr :8000
# macOS/Linux: lsof -i :8000
```

---

### Email Service Issues

#### "Failed to send email: SMTP authentication failed"
```
Solution 1: Use Gmail app-specific password (16 chars), not regular password
Solution 2: Enable "Less secure apps" (if not using 2FA)
Solution 3: Check credentials in serverless/.env
```

#### "Email service not responding (http://localhost:3000)"
```bash
# Check if serverless is running:
npm run offline

# Check if port 3000 is available:
# Windows: netstat -ano | findstr :3000
# macOS/Linux: lsof -i :3000
```

---

### Google Calendar Issues

#### "Invalid credentials for Google Calendar"
```
Solution 1: Re-download credentials JSON from Google Cloud Console
Solution 2: Ensure GOOGLE_CLIENT_ID and SECRET are correct
Solution 3: Check OAuth callback URL matches
```

#### "Calendar event not created"
```bash
# Check if user is connected:
# Visit: http://localhost:8000/api/calendar/google/check/

# Try reconnecting:
# Click "Disconnect" then "Connect Google Calendar" again
```

---

### General Issues

#### "CORS error when calling API"
```
Check hms_project/settings.py CORS_ALLOWED_ORIGINS
Add your domain/port if needed
```

#### "Static files not found (CSS/JS not loading)"
```bash
python manage.py collectstatic --noinput
```

#### "Login not working"
```bash
# Check if user exists:
python manage.py shell
>>> from django.contrib.auth import get_user_model
>>> User = get_user_model()
>>> User.objects.filter(email='your-email@example.com')

# Check password:
>>> user = User.objects.get(email='your-email@example.com')
>>> user.check_password('your-password')
True
```

---

## Verification Checklist

### System Running
- [ ] Django server running on http://localhost:8000
- [ ] Serverless service running on http://localhost:3000
- [ ] PostgreSQL database created and connected
- [ ] Admin interface accessible at /admin/

### Features Working
- [ ] Doctor signup creates account
- [ ] Patient signup creates account
- [ ] Login works for both roles
- [ ] Doctor can create availability
- [ ] Patient can view available doctors
- [ ] Patient can book appointment
- [ ] Slot blocked after booking
- [ ] Patient cannot double-book
- [ ] Patient can cancel booking
- [ ] Slot freed after cancellation
- [ ] Doctor can view bookings
- [ ] Email notifications sent
- [ ] Google Calendar events created
- [ ] Google Calendar events deleted

### Code Quality
- [ ] All endpoints accessible
- [ ] No SQL errors in logs
- [ ] No JavaScript console errors
- [ ] Form validation working
- [ ] Error messages clear
- [ ] Database transactions atomic

---

**System is ready for demonstration and production deployment!** 🚀
