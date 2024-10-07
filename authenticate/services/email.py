from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.conf import settings

class Email:
    def __init__(self , email , content):
        self.email = email
        self.content = content

    @staticmethod
    def send_review_email( email , code):
        email_context = {
            "email": email,
            "code": code,
        }

        email_subject = "thank you for your review"
        email_body = render_to_string("message.txt", email_context)
        from_email = settings.EMAIL_HOST_USER

        try:
            send_mail(subject=email_subject, message=email_body, from_email=from_email, recipient_list=[email])
            return True
        except Exception as e:
            return f"An error occurred while sending the email: {e}"