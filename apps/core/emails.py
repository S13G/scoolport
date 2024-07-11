from django.contrib.auth import get_user_model
from django.template.loader import render_to_string

from utils.emails import send_email

User = get_user_model()


def send_otp_email(otp_secret: str, recipient: str or User, template=None) -> None:
    # Determine email address based on the type of recipient
    if isinstance(recipient, User):
        email_address = recipient.email
    else:
        email_address = recipient

    subject = 'One-Time Password (OTP) Verification'
    recipients = [email_address]
    context = {'email': email_address}
    message = render_to_string(template, context)

    # Send the email
    send_email(subject, recipients, message=message, template=template, context=context)
