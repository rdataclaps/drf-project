import os
from django.core.mail import EmailMessage


class Util:
    @staticmethod
    def send_email(dataa):
        email=EmailMessage(
            subject=dataa['subject'],
            body=dataa['body'],
            from_email=os.environ.get('EMAIL_FROM'),
            to=[dataa['to_email']]
        )
        email.send(dataa)