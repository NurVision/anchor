from django.conf import settings

from apps.common.tasks.send_mail_task import send_email_task
from apps.users.services.user_services import UserService


def send_validation_email(email: str, link: str):
    try:
        print(">>>>>>>>>>>>>>>>>> Email", settings.DEFAULT_FROM_EMAIL)
        send_email_task.delay(
            subject="Validation Email from mNews",
            message=f"Click the link to validate your email for the mNews: {link}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
        )
    except Exception:
        pass


def send_welcome_email(email: str):
    try:
        send_email_task.delay(
            subject="Welcome to mNews",
            message=f"You have been successfully logged in to mNews!",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
        )
    except Exception:
        pass


def send_restore_user_email(email: str, restore_link: str):
    try:
        send_email_task.delay(
            subject="Restore your account",
            message=f"To restore your account, click the following link: {restore_link}",
            from_email=getattr(settings, "DEFAULT_FROM_EMAIL", None),
            recipient_list=[email],
        )
    except Exception:
        pass


def send_reset_password_email(user):
    try:
        otp = UserService.generate_otp(user)
        send_email_task.delay(
            subject="Reset Password",
            message=f"Someone, hopefully you have tried to reset your password! Below there is one time password to complete this.\n\n {otp}",
            from_email=getattr(settings, "DEFAULT_FROM_EMAIL", None),
            recipient_list=[user.email],
        )

    except Exception:
        pass
