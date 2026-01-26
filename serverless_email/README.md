# HMS Serverless Email Service

This is a serverless email service for the HMS platform using AWS Lambda and Serverless Framework.

## Setup

1. Install dependencies:
```bash
npm install -g serverless
npm install
```

2. Copy `.env.example` to `.env` and set your Gmail credentials:
```bash
cp .env.example .env
```

3. Configure Gmail:
- Enable 2-Step Verification on your Gmail account
- Generate an [App Password](https://myaccount.google.com/apppasswords)
- Use the 16-character password as `GMAIL_PASSWORD`

## Development

Run locally with serverless-offline:
```bash
serverless offline start
```

The service will be available at `http://localhost:3000`

## Endpoints

### POST /send-email

Sends an email based on the action type.

**Request Body:**
```json
{
  "action": "SIGNUP_WELCOME|BOOKING_CONFIRMATION|BOOKING_CANCELLATION",
  "patient_email": "patient@example.com",
  "patient_name": "John Doe",
  "doctor_name": "Dr. Jane Smith",
  "date": "2024-02-15",
  "start_time": "10:00:00",
  "end_time": "11:00:00"
}
```

**Response:**
```json
{
  "message": "Email sent successfully"
}
```

## Deployment

```bash
serverless deploy
```

## Environment Variables

- `GMAIL_USER`: Gmail address to send from
- `GMAIL_PASSWORD`: Gmail app-specific password
