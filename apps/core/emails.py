from django.template.loader import render_to_string

from utils.emails import send_email


def send_account_email(recipient: str, full_name: str, password: str, template=None) -> None:
    email_address = recipient

    subject = 'Account Details'
    recipients = [email_address]
    context = {'email_address': email_address, "full_name": full_name, "password": password}
    message = render_to_string(template, context)
    # Send the email
    send_email(subject, recipients, message=message, template=template, context=context)
