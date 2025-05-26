import os

from apps.employee.models import Employee as User
from utils.services.jwt_service import (ActivateToken, JWTService)
from django.contrib.auth import get_user_model
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template

UserModel: User = get_user_model()


class EmailService:
    """Handles sending HTML emails to users."""

    @staticmethod
    def __send_email(to: str, template_name: str, context: dict, subject='') -> None:
        """Sends an HTML email using a template and context."""
        template = get_template(template_name)
        html_content = template.render(context)
        msg = EmailMultiAlternatives(subject, from_email=os.environ.get('EMAIL_HOST_USER'), to=[to])
        msg.attach_alternative(html_content, 'text/html')
        msg.send()

    @classmethod
    def register_email(cls, user) -> None:
        """Sends registration confirmation email to the given user."""
        token = JWTService.create_token(user, ActivateToken)
        url = f'http://localhost:3000/verify-email/{token}'
        cls.__send_email(user, 'register_email.html', {'name': user, 'url': url}, 'Register')
