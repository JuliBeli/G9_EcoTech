# post_app/services/email_service.py
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
import logging

logger = logging.getLogger(__name__)


class EmailService:
    @staticmethod
    def send_password_reset_code(user, code):
        subject = 'Verification code of password reset'
        message = f'Your verification code for resetting password is :{code},it expires in 10 minutes.'

        try:
            print(f"尝试发送邮件到: {user.email}")  # 调试信息
            print(f"验证码: {code}")  # 调试信息
            print(f"发件人: {settings.DEFAULT_FROM_EMAIL}")  # 调试信息

            send_mail(
                subject=subject,
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                fail_silently=False,
            )
            logger.info(f"Password reset code sent to {user.email}")
            return True
        except Exception as e:
            logger.error(f"Failed to send email to {user.email}: {str(e)}")
            return False