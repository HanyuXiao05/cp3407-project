from flask import current_app, request
from flask_mail import Message, Mail

mail = Mail()

def send_email(to, subject, template):
    msg = Message(
        subject,
        recipients=[to],
        html=template,
        sender=current_app.config['MAIL_USERNAME']
    )
    mail.send(msg)

def send_confirmation_email(to, token):
    confirm_url = f"{request.host_url}auth/confirm/{token}"
    template = f'''
    <p>Welcome to JCU Gym! Please click the link below to confirm your email address:</p>
    <p><a href="{confirm_url}">Confirm Email</a></p>
    <p>If you did not make this request, please ignore this email.</p>
    '''
    send_email(to, 'Please confirm your email', template)

def send_booking_confirmation(to, booking_details):
    template = f'''
    <h2>Booking Confirmation</h2>
    <p>Your session has been booked successfully!</p>
    <p>Details:</p>
    <ul>
        <li>Date: {booking_details['date']}</li>
        <li>Time: {booking_details['time']}</li>
        <li>Session: {booking_details['session_name']}</li>
    </ul>
    '''
    send_email(to, 'Booking Confirmation', template)

def send_booking_reminder(to, booking_details):
    template = f'''
    <h2>Session Reminder</h2>
    <p>This is a reminder for your upcoming session:</p>
    <ul>
        <li>Date: {booking_details['date']}</li>
        <li>Time: {booking_details['time']}</li>
        <li>Session: {booking_details['session_name']}</li>
    </ul>
    <p>We look forward to seeing you!</p>
    '''
    send_email(to, 'Session Reminder', template) 