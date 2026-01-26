# QUICK START GUIDE - Hospital Management System

## 🚀 5-Minute Setup

### Prerequisites
- Python 3.9+
- PostgreSQL
- Node.js (for serverless)
- Git

### Step 1: Database Setup
```bash
# Create PostgreSQL database
createdb hms_db

# Or using psql
psql -U postgres -c "CREATE DATABASE hms_db;"
```

### Step 2: Backend Setup
```bash
cd hms_backend

# Create virtual environment
python -m venv venv

# Activate (Windows: venv\Scripts\activate)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure .env
cp .env.example .env
# Edit .env with your PostgreSQL credentials

# Run migrations
python manage.py migrate

# Create admin account
python manage.py createsuperuser

# Start server
python manage.py runserver
```

Backend will run at: **http://localhost:8000**

### Step 3: Serverless Email Setup
```bash
cd serverless_email

# Install dependencies
npm install

# Configure .env
cp .env.example .env
# Edit .env with Gmail credentials

# Start serverless offline
npm run offline
```

Email service will run at: **http://localhost:3000**

---

## 🔐 User Registration

### Doctor Account
1. Go to: `http://localhost:8000/api/users/doctor-signup/`
2. Fill in details:
   - First Name: John
   - Last Name: Doe
   - Email: doctor@example.com
   - Password: SecurePass123

### Patient Account
1. Go to: `http://localhost:8000/api/users/patient-signup/`
2. Fill in details:
   - First Name: Jane
   - Last Name: Smith
   - Email: patient@example.com
   - Password: SecurePass123

---

## 📅 Creating Doctor Availability

1. **Login as Doctor**: `http://localhost:8000/api/users/login/`
2. Go to **Doctor Dashboard** (link provided after login)
3. Fill in availability:
   - Date: 2024-02-15
   - Start Time: 10:00
   - End Time: 11:00
4. Click "Create Slot"

---

## 🏥 Booking Appointment (Patient)

1. **Login as Patient**: `http://localhost:8000/api/users/login/`
2. Go to **Patient Dashboard**
3. Browse "Available Doctors"
4. Click on a doctor to see their slots
5. Click time slot to open booking modal
6. Review details and click "Confirm Booking"
7. Check email for confirmation

---

## 📧 Email Notifications

The serverless email service sends emails for:

### Signup Welcome
- Sent when user creates account
- Contains login link

### Booking Confirmation
- Sent to patient when booking confirmed
- Includes doctor name, date, time

### Booking Cancellation
- Sent when appointment cancelled
- Allows rebooking

**Note**: Requires valid Gmail credentials in `.env`

---

## 🗓️ Google Calendar Integration

1. Create Google OAuth credentials:
   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Create project, enable Calendar API
   - Create OAuth 2.0 Desktop app credentials
   - Download JSON credentials

2. Add to `.env`:
   ```
   GOOGLE_CLIENT_ID=your-client-id
   GOOGLE_CLIENT_SECRET=your-client-secret
   ```

3. In Doctor Dashboard, click "Connect Google Calendar"
4. Authorize and events will sync automatically

---

## 🧪 Testing Checklist

### Authentication
- [ ] Doctor signup works
- [ ] Patient signup works
- [ ] Email validation works
- [ ] Login with email works
- [ ] Session expires correctly

### Doctor Features
- [ ] Can create availability slots
- [ ] Can view their own slots
- [ ] Can edit availability
- [ ] Can delete availability
- [ ] Can view patient bookings

### Patient Features
- [ ] Can view available doctors
- [ ] Can see doctor availability
- [ ] Can book appointments
- [ ] Cannot book same slot twice
- [ ] Can cancel bookings
- [ ] Slot becomes available again after cancel

### Notifications
- [ ] Signup email received
- [ ] Booking confirmation email received
- [ ] Cancellation email received

### Google Calendar
- [ ] Can connect to Google
- [ ] Events appear in Google Calendar
- [ ] Doctor and patient both see event
- [ ] Event deleted on booking cancellation

---

## 📍 API Endpoints

### Authentication
```
POST /api/users/api/doctor-signup/
POST /api/users/api/patient-signup/
POST /api/users/api/login/
POST /api/users/api/logout/
```

### Availability
```
POST /api/availability/create/
GET /api/availability/my-slots/
GET /api/availability/available-doctors/
GET /api/availability/doctor/<id>/
```

### Bookings
```
POST /api/bookings/create/
GET /api/bookings/my-bookings/
POST /api/bookings/<id>/cancel/
```

### Calendar
```
GET /api/calendar/google/auth-url/
GET /api/calendar/google/check/
POST /api/calendar/google/disconnect/
```

---

## 🐛 Troubleshooting

### PostgreSQL Connection Error
```
Error: FATAL: authentication failed
Solution: Check DB_USER and DB_PASSWORD in .env
```

### Serverless Email Not Sending
```
Error: SMTP authentication failed
Solution: Use Gmail app-specific password, not regular password
```

### Google Calendar Error
```
Error: Invalid credentials
Solution: Ensure credentials are updated in .env and Google OAuth app is configured
```

### Port Already in Use
```
Error: port 8000 already in use
Solution: Kill process or use: python manage.py runserver 8001
```

---

## 📝 Admin Panel

Access at: `http://localhost:8000/admin/`

Use superuser credentials to:
- View all users
- Create test data
- Monitor bookings
- Manage availability slots

---

## 💡 Demo Flow (10 minutes)

### 1. Signup (1 min)
- Show doctor signup
- Show patient signup
- Show confirmation emails

### 2. Setup Availability (2 min)
- Login as doctor
- Create 3-4 availability slots
- Show different time ranges

### 3. Patient Booking (3 min)
- Login as patient
- Browse doctors
- Select slot
- Complete booking
- Show confirmation email

### 4. Google Calendar (2 min)
- Connect Google Calendar
- Show event appears in calendar
- Cancel and show removal

### 5. Code Walkthrough (2 min)
- Show models (User, Availability, Booking)
- Show booking validation logic
- Show email service integration

---

## 📚 File Structure

```
hms_backend/
├── users/              # Authentication
├── availability/       # Doctor slots
├── bookings/          # Appointment bookings
├── calendar_integration/  # Google Calendar
├── templates/         # HTML templates
├── manage.py          # Django CLI
└── requirements.txt   # Dependencies

serverless_email/
├── handler.py         # Lambda handler
├── serverless.yml     # Configuration
└── requirements.txt   # Python deps
```

---

## 🚀 Deployment (Optional)

### Backend (Heroku)
```bash
# Create Procfile
echo "web: gunicorn hms_project.wsgi" > Procfile

# Deploy
heroku create your-app-name
git push heroku main
heroku run python manage.py migrate
```

### Serverless (AWS Lambda)
```bash
cd serverless_email
npm install -g serverless
serverless deploy
```

---

## 📞 Support

For issues, check:
1. Django logs: `python manage.py runserver`
2. Serverless logs: `serverless offline start`
3. Browser console: Press F12
4. Database: `psql hms_db`

---

**Ready to demo! 🎉**
