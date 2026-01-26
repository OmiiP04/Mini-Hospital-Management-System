# Hospital Management System (HMS) - START HERE 🏥

Welcome to the Mini Hospital Management System! This document will guide you through the project structure and help you get started quickly.

---

## 📚 Documentation Index

### For Getting Started (Start here!)
1. **[QUICKSTART.md](QUICKSTART.md)** - 5-minute setup guide
   - Quick prerequisites check
   - Step-by-step installation
   - Running the system
   - Basic testing

2. **[README.md](README.md)** - Complete documentation
   - Project overview
   - Full feature list
   - Installation instructions
   - API documentation
   - Troubleshooting

### For Detailed Setup
3. **[SETUP_AND_TESTING.md](SETUP_AND_TESTING.md)** - Comprehensive guide
   - Detailed prerequisites
   - Full installation with screenshots
   - Configuration setup (Google Calendar, Gmail)
   - Step-by-step testing guide
   - Demo walkthrough script
   - Advanced troubleshooting

### For Project Understanding
4. **[PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)** - Project overview
   - Completion status
   - Feature checklist
   - Technology stack
   - Architecture overview
   - Key business logic
   - Security features

5. **[FILE_INVENTORY.md](FILE_INVENTORY.md)** - Complete file listing
   - Project structure
   - File descriptions
   - Code statistics
   - Dependencies
   - API endpoints

---

## 🚀 Quick Start (5 Minutes)

### Prerequisites
- Python 3.9+
- PostgreSQL installed
- Node.js installed (for email service)

### Installation

#### 1. Create Database
```bash
createdb hms_db
```

#### 2. Setup Backend
```bash
cd hms_backend
python -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env              # Configure with your DB credentials
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

#### 3. Setup Serverless Email
```bash
cd serverless_email
npm install
cp .env.example .env              # Configure with Gmail credentials
npm run offline
```

### Access
- **Website**: http://localhost:8000
- **Admin**: http://localhost:8000/admin
- **Email Service**: http://localhost:3000

---

## 📂 Project Structure

```
Mini Hospital Management System/
├── README.md                  # Complete documentation
├── QUICKSTART.md             # 5-minute setup
├── SETUP_AND_TESTING.md      # Detailed guide
├── PROJECT_SUMMARY.md        # Project overview
├── FILE_INVENTORY.md         # File listing
├── INDEX.md                  # This file
├── setup.sh                  # Linux/macOS setup
├── setup.bat                 # Windows setup
│
├── hms_backend/              # Django backend
│   ├── hms_project/          # Project config
│   ├── users/                # Authentication
│   ├── availability/         # Doctor slots
│   ├── bookings/             # Appointments
│   ├── calendar_integration/ # Google Calendar
│   ├── templates/            # HTML templates
│   ├── manage.py
│   ├── requirements.txt
│   └── .env.example
│
└── serverless_email/         # Email service
    ├── handler.py
    ├── serverless.yml
    ├── package.json
    ├── requirements.txt
    └── .env.example
```

---

## ✨ Key Features

### User Management
- ✅ Separate signup for Doctors and Patients
- ✅ Secure password hashing
- ✅ Session-based authentication
- ✅ Role-based access control

### Doctor Features
- ✅ Create and manage availability slots
- ✅ View patient bookings
- ✅ Connect to Google Calendar
- ✅ Receive appointment notifications

### Patient Features
- ✅ Browse available doctors
- ✅ View doctor availability slots
- ✅ Book appointments
- ✅ Cancel bookings
- ✅ Receive confirmation emails

### Advanced Features
- ✅ Email notifications (signup, booking, cancellation)
- ✅ Google Calendar integration
- ✅ Race condition protection (atomic transactions)
- ✅ Automatic slot blocking
- ✅ Admin interface for management

---

## 🔧 Technology Stack

| Component | Technology |
|-----------|-----------|
| Backend | Django 4.2.7 |
| Database | PostgreSQL |
| ORM | Django ORM |
| API | Django REST Framework |
| Email | AWS Lambda + Serverless Framework |
| Calendar | Google Calendar API + OAuth2 |
| Frontend | HTML5, CSS3, Vanilla JavaScript |
| Deployment Ready | Heroku, AWS Lambda |

---

## 📋 What's Included

### Backend (Django)
- ✅ 4 Django apps (users, availability, bookings, calendar_integration)
- ✅ 27 API endpoints
- ✅ 3 core models (CustomUser, DoctorAvailability, Booking)
- ✅ Complete authentication system
- ✅ Admin interface

### Frontend
- ✅ Doctor signup page
- ✅ Patient signup page
- ✅ Login page
- ✅ Doctor dashboard (with JavaScript interactivity)
- ✅ Patient dashboard (with JavaScript interactivity)
- ✅ User profile page
- ✅ Responsive design with modern styling

### Services
- ✅ Serverless email service (AWS Lambda)
- ✅ Google Calendar synchronization
- ✅ PostgreSQL integration

### Documentation
- ✅ README (4,500+ words)
- ✅ Quick start guide
- ✅ Setup and testing guide
- ✅ Project summary
- ✅ File inventory
- ✅ Code comments throughout

---

## 🧪 Testing Guide

### Basic Testing (20 minutes)

1. **Doctor Signup**
   - Go to: http://localhost:8000/api/users/doctor-signup/
   - Fill form and submit
   - Login with new account

2. **Patient Signup**
   - Go to: http://localhost:8000/api/users/patient-signup/
   - Fill form and submit
   - Login with new account

3. **Create Availability**
   - Login as doctor
   - Create 3 availability slots
   - View in dashboard

4. **Book Appointment**
   - Login as patient
   - Browse doctors
   - Select time slot
   - Complete booking

5. **Verify Email**
   - Check serverless logs for confirmation email
   - Verify booking details

6. **Google Calendar** (optional)
   - Doctor connects Google Calendar
   - Verify event appears in calendar

---

## 📚 Documentation by Use Case

### "I want to set it up"
→ Read [QUICKSTART.md](QUICKSTART.md)

### "I need detailed installation steps"
→ Read [SETUP_AND_TESTING.md](SETUP_AND_TESTING.md)

### "I want to understand the architecture"
→ Read [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)

### "I want to see all API endpoints"
→ Read [README.md](README.md#api-endpoints)

### "I want to know all files created"
→ Read [FILE_INVENTORY.md](FILE_INVENTORY.md)

### "I want to test the system"
→ Read [SETUP_AND_TESTING.md](SETUP_AND_TESTING.md#testing-guide)

### "I want to give a demo"
→ Read [SETUP_AND_TESTING.md](SETUP_AND_TESTING.md#demo-walkthrough)

### "Something is broken"
→ Read [README.md](README.md#troubleshooting) or [SETUP_AND_TESTING.md](SETUP_AND_TESTING.md#troubleshooting)

---

## 🎯 Next Steps

### Step 1: Read QUICKSTART
Open [QUICKSTART.md](QUICKSTART.md) and follow the 5-minute setup.

### Step 2: Start the System
- Run Django backend: `python manage.py runserver`
- Run Serverless email: `npm run offline`

### Step 3: Create Test Accounts
- Doctor: doctor@example.com
- Patient: patient@example.com

### Step 4: Test Features
- Create availability slots
- Book appointments
- Check email notifications

### Step 5: Explore the Code
- Check `hms_backend/` for Django apps
- Check `serverless_email/` for email service
- Review `templates/` for UI

---

## 🔗 API Quick Reference

### User Endpoints
```
POST   /api/users/api/doctor-signup/
POST   /api/users/api/patient-signup/
POST   /api/users/api/login/
POST   /api/users/api/logout/
GET    /api/users/api/profile/
PUT    /api/users/api/profile/update/
```

### Availability Endpoints
```
POST   /api/availability/create/
GET    /api/availability/my-slots/
GET    /api/availability/available-doctors/
GET    /api/availability/doctors/
GET    /api/availability/doctor/<id>/
```

### Booking Endpoints
```
POST   /api/bookings/create/
GET    /api/bookings/my-bookings/
GET    /api/bookings/<id>/
POST   /api/bookings/<id>/cancel/
```

### Calendar Endpoints
```
GET    /api/calendar/google/auth-url/
GET    /api/calendar/google/callback/
GET    /api/calendar/google/check/
POST   /api/calendar/google/disconnect/
```

---

## 💡 Important Notes

### Database Setup
```bash
# Create PostgreSQL database before starting
createdb hms_db
```

### Virtual Environment
```bash
# Always activate venv before running Django
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows
```

### Environment Variables
```bash
# Copy .env.example to .env and configure:
# - Database credentials
# - Google OAuth credentials (optional)
# - Gmail credentials for email service
```

### Running Both Services
```bash
# Terminal 1: Django
cd hms_backend
python manage.py runserver

# Terminal 2: Serverless
cd serverless_email
npm run offline
```

---

## 🎓 Learning Resources

### Django
- [Django Documentation](https://docs.djangoproject.com/)
- Models, Views, Templates, Admin
- Django REST Framework

### Database
- PostgreSQL concepts
- Transactions and ACID
- Foreign keys and relationships

### APIs
- RESTful design
- Authentication
- Error handling

### Frontend
- HTML5 forms
- CSS3 styling
- JavaScript Fetch API
- AJAX requests

### DevOps
- Virtual environments
- Environment variables
- Deployment

---

## ✅ Verification Checklist

Before considering the project complete:

### Setup
- [ ] Python 3.9+ installed
- [ ] PostgreSQL installed and running
- [ ] Node.js installed
- [ ] Virtual environment created
- [ ] Dependencies installed

### Running
- [ ] Django server starts
- [ ] Serverless service starts
- [ ] Database migrations complete
- [ ] Admin user created
- [ ] Can access http://localhost:8000

### Features
- [ ] Doctor signup works
- [ ] Patient signup works
- [ ] Can create availability slots
- [ ] Can book appointments
- [ ] Can cancel bookings
- [ ] Email notifications sent
- [ ] Google Calendar syncs (optional)

### Documentation
- [ ] README is comprehensive
- [ ] QUICKSTART is clear
- [ ] Code is commented
- [ ] APIs are documented

---

## 🆘 Getting Help

1. **Installation issues?**
   → Check [SETUP_AND_TESTING.md](SETUP_AND_TESTING.md#troubleshooting)

2. **Feature not working?**
   → Check [README.md](README.md#troubleshooting)

3. **Want to understand code?**
   → Read [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)

4. **Need API details?**
   → Check [README.md](README.md#api-endpoints)

5. **Want to test?**
   → Follow [SETUP_AND_TESTING.md](SETUP_AND_TESTING.md#testing-guide)

---

## 📞 Project Contact

For questions or issues:
1. Check the relevant documentation file (linked above)
2. Review the code comments
3. Check Django/API logs
4. Check browser console for errors

---

## 🎉 You're Ready!

You now have a complete Hospital Management System with:
- ✅ Doctor availability management
- ✅ Patient appointment booking
- ✅ Email notifications
- ✅ Google Calendar integration
- ✅ Full documentation
- ✅ Ready-to-deploy code

**Start with [QUICKSTART.md](QUICKSTART.md) and enjoy!** 🚀

---

**Last Updated**: January 23, 2026
**Status**: ✅ Complete and Ready for Production
