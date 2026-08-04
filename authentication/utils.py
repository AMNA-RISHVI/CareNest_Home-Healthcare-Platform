from django.core.mail import EmailMessage
from django.template.loader import render_to_string


def send_verification_email(request, user, verification_url):

    subject = "Verify Your CareNest Account"

    message = render_to_string(
        "authentication/verify_email.html",
        {
            "user": user,
            "verification_url": verification_url,
        }
    )

    email = EmailMessage(
        subject,
        message,
        to=[user.email],
    )

    email.content_subtype = "html"

    email.send()


def send_password_reset_email(request, user, reset_url):

    subject = "Reset Your CareNest Password"

    message = render_to_string(
        "authentication/password_reset_email.html",
        {
            "user": user,
            "reset_url": reset_url,
        }
    )

    email = EmailMessage(
        subject,
        message,
        to=[user.email],
    )

    email.content_subtype = "html"

    email.send()