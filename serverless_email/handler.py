import json
import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

def send_email(event, context):
    """
    Main Lambda handler for sending emails
    Expected body structure:
    {
        "action": "SIGNUP_WELCOME" | "BOOKING_CONFIRMATION" | "BOOKING_CANCELLATION",
        "recipient_email": "email@example.com",
        "recipient_name": "Name",
        "doctor_name": "Dr. Name" (for booking emails),
        "patient_name": "Patient Name" (for booking emails),
        "date": "YYYY-MM-DD" (for booking emails),
        "start_time": "HH:MM:SS" (for booking emails),
        "end_time": "HH:MM:SS" (for booking emails)
    }
    """
    
    try:
        body = json.loads(event.get('body', '{}'))
        action = body.get('action')
        
        if action == 'SIGNUP_WELCOME':
            return send_welcome_email(body)
        elif action == 'BOOKING_CONFIRMATION':
            return send_booking_confirmation(body)
        elif action == 'BOOKING_CANCELLATION':
            return send_booking_cancellation(body)
        else:
            return error_response(400, f'Unknown action: {action}')
    
    except Exception as e:
        print(f"Error: {str(e)}")
        return error_response(500, f'Email sending failed: {str(e)}')


def send_welcome_email(data):
    """Send welcome email to new user"""
    recipient_email = data.get('patient_email') or data.get('doctor_email')
    recipient_name = data.get('patient_name') or data.get('doctor_name')
    user_type = data.get('user_type', 'User')
    
    subject = f"Welcome to HMS, {recipient_name}!"
    
    html_body = f"""
    <html>
        <body style="font-family: Arial, sans-serif;">
            <h2>Welcome to Hospital Management System (HMS)!</h2>
            <p>Dear {recipient_name},</p>
            <p>Your account as a {user_type} has been successfully created.</p>
            <p>You can now log in and start using the HMS platform.</p>
            <p>
                <strong>Dashboard URL:</strong> <a href="http://localhost:8000">Click here to access HMS</a>
            </p>
            <p>If you have any questions, please contact our support team.</p>
            <br>
            <p>Best regards,<br>HMS Team</p>
        </body>
    </html>
    """
    
    return send_smtp_email(recipient_email, subject, html_body)


def send_booking_confirmation(data):
    """Send booking confirmation email"""
    patient_email = data.get('patient_email')
    patient_name = data.get('patient_name')
    doctor_name = data.get('doctor_name')
    date = data.get('date')
    start_time = data.get('start_time')
    end_time = data.get('end_time')
    
    subject = f"Appointment Confirmed with Dr. {doctor_name}"
    
    html_body = f"""
    <html>
        <body style="font-family: Arial, sans-serif;">
            <h2>Appointment Confirmation</h2>
            <p>Dear {patient_name},</p>
            <p>Your appointment has been confirmed!</p>
            <table style="border-collapse: collapse; margin: 20px 0;">
                <tr style="background-color: #f2f2f2;">
                    <td style="border: 1px solid #ddd; padding: 10px;"><strong>Doctor:</strong></td>
                    <td style="border: 1px solid #ddd; padding: 10px;">Dr. {doctor_name}</td>
                </tr>
                <tr>
                    <td style="border: 1px solid #ddd; padding: 10px;"><strong>Date:</strong></td>
                    <td style="border: 1px solid #ddd; padding: 10px;">{date}</td>
                </tr>
                <tr style="background-color: #f2f2f2;">
                    <td style="border: 1px solid #ddd; padding: 10px;"><strong>Time:</strong></td>
                    <td style="border: 1px solid #ddd; padding: 10px;">{start_time} - {end_time}</td>
                </tr>
            </table>
            <p>Please arrive 10 minutes early. If you need to reschedule, please visit your dashboard.</p>
            <p>Best regards,<br>HMS Team</p>
        </body>
    </html>
    """
    
    return send_smtp_email(patient_email, subject, html_body)


def send_booking_cancellation(data):
    """Send booking cancellation email"""
    patient_email = data.get('patient_email')
    patient_name = data.get('patient_name')
    doctor_name = data.get('doctor_name')
    date = data.get('date')
    start_time = data.get('start_time')
    end_time = data.get('end_time')
    
    subject = f"Appointment Cancelled - Dr. {doctor_name}"
    
    html_body = f"""
    <html>
        <body style="font-family: Arial, sans-serif;">
            <h2>Appointment Cancellation</h2>
            <p>Dear {patient_name},</p>
            <p>Your appointment has been cancelled.</p>
            <table style="border-collapse: collapse; margin: 20px 0;">
                <tr style="background-color: #f2f2f2;">
                    <td style="border: 1px solid #ddd; padding: 10px;"><strong>Doctor:</strong></td>
                    <td style="border: 1px solid #ddd; padding: 10px;">Dr. {doctor_name}</td>
                </tr>
                <tr>
                    <td style="border: 1px solid #ddd; padding: 10px;"><strong>Date:</strong></td>
                    <td style="border: 1px solid #ddd; padding: 10px;">{date}</td>
                </tr>
                <tr style="background-color: #f2f2f2;">
                    <td style="border: 1px solid #ddd; padding: 10px;"><strong>Time:</strong></td>
                    <td style="border: 1px solid #ddd; padding: 10px;">{start_time} - {end_time}</td>
                </tr>
            </table>
            <p>You can book another appointment through your HMS dashboard.</p>
            <p>If you have any questions, contact our support team.</p>
            <p>Best regards,<br>HMS Team</p>
        </body>
    </html>
    """
    
    return send_smtp_email(patient_email, subject, html_body)


def send_smtp_email(recipient_email, subject, html_body):
    """Send email using SMTP"""
    try:
        sender_email = os.environ.get('GMAIL_USER', 'your-email@gmail.com')
        sender_password = os.environ.get('GMAIL_PASSWORD', 'your-app-password')
        
        # Create message
        message = MIMEMultipart("alternative")
        message["Subject"] = subject
        message["From"] = sender_email
        message["To"] = recipient_email
        
        # Create plain text and HTML versions
        text = html_body.replace('<html>', '').replace('</html>', '').replace('<body>', '').replace('</body>', '').replace('<br>', '\n')
        part1 = MIMEText(text, "plain")
        part2 = MIMEText(html_body, "html")
        
        message.attach(part1)
        message.attach(part2)
        
        # Send email via Gmail SMTP
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, recipient_email, message.as_string())
        
        return success_response({'message': 'Email sent successfully'})
    
    except Exception as e:
        print(f"SMTP Error: {str(e)}")
        return error_response(500, f'Failed to send email: {str(e)}')


def success_response(data):
    """Return success response"""
    return {
        'statusCode': 200,
        'body': json.dumps(data),
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        }
    }


def error_response(status_code, message):
    """Return error response"""
    return {
        'statusCode': status_code,
        'body': json.dumps({'error': message}),
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        }
    }
