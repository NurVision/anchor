from django.conf import settings
from django.core.mail import EmailMultiAlternatives

from apps.common.tasks.send_mail_task import send_email_task
from apps.users.services.user_services import UserService


def send_validation_email(email: str, validation_link: str, deletion_link: str) -> bool:
    """
    Send a verification email with validation and deletion links.

    Args:
        email: Recipient email address
        validation_link: URL to verify the account
        deletion_link: URL to cancel the account request

    Returns:
        bool: True if email was sent successfully, False otherwise
    """
    subject = "Welcome to mNews – Verify Your Email"
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [email]

    # Plain text version
    text_message = (
        f"Welcome to mNews!\n\n"
        f"To complete your registration, please verify your email address.\n\n"
        f"Verify your account: {validation_link}\n"
        f"Cancel account request: {deletion_link}\n\n"
        f"If you did not request this registration, you can safely ignore this email."
    )

    # HTML version - more concise and maintainable
    html_message = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
    </head>
    <body style="margin:0; padding:20px; font-family:Arial,sans-serif; background-color:#f4f4f4;">
        <div style="max-width:600px; margin:0 auto; background-color:#ffffff; padding:30px; border-radius:8px; box-shadow:0 2px 4px rgba(0,0,0,0.1);">
            <h2 style="color:#0073e6; margin-top:0;">Welcome to mNews!</h2>

            <p style="color:#333; line-height:1.6; margin:20px 0;">
                We received a request to create an account with this email address. 
                Please confirm by verifying your email.
            </p>

            <table cellpadding="0" cellspacing="0" style="margin:30px 0;">
                <tr>
                    <td style="padding:12px 24px; background-color:#0073e6; border-radius:5px;">
                        <a href="{validation_link}" style="color:#ffffff; text-decoration:none; font-weight:bold; display:block;">
                            ✅ Verify My Email
                        </a>
                    </td>
                </tr>
            </table>

            <p style="color:#333; line-height:1.6; margin:20px 0;">
                If you did not request this account, you can cancel it:
            </p>

            <table cellpadding="0" cellspacing="0" style="margin:20px 0;">
                <tr>
                    <td style="padding:12px 24px; background-color:#cc0000; border-radius:5px;">
                        <a href="{deletion_link}" style="color:#ffffff; text-decoration:none; font-weight:bold; display:block;">
                            ❌ Cancel Account Request
                        </a>
                    </td>
                </tr>
            </table>

            <hr style="margin:30px 0; border:none; border-top:1px solid #ddd;" />

            <p style="font-size:12px; color:#777; line-height:1.4;">
                This message was sent to {email} because someone used this address to sign up for mNews. 
                If this was not you, simply ignore this email and no account will be created.
            </p>
        </div>
    </body>
    </html>
    """

    try:
        msg = EmailMultiAlternatives(subject, text_message, from_email, recipient_list)
        msg.attach_alternative(html_message, "text/html")
        msg.send(fail_silently=False)
        return True
    except Exception as e:
        return False


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


def send_password_reset_email(email: str, reset_link: str) -> bool:
    """
    Send a password reset email with a secure link.

    Args:
        email: Recipient email address
        reset_link: URL to reset the password

    Returns:
        bool: True if email was sent successfully, False otherwise
    """
    subject = "mNews – Password Reset Request"
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [email]

    text_message = (
        f"Password Reset Request\n\n"
        f"We received a request to reset your password for your mNews account.\n\n"
        f"Click the link below to reset your password:\n"
        f"{reset_link}\n\n"
        f"This link will expire in 1 hour.\n\n"
        f"If you did not request a password reset, please ignore this email. "
        f"Your password will remain unchanged."
    )

    html_message = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
    </head>
    <body style="margin:0; padding:20px; font-family:Arial,sans-serif; background-color:#f4f4f4;">
        <div style="max-width:600px; margin:0 auto; background-color:#ffffff; padding:30px; border-radius:8px; box-shadow:0 2px 4px rgba(0,0,0,0.1);">
            <h2 style="color:#0073e6; margin-top:0;">Password Reset Request</h2>

            <p style="color:#333; line-height:1.6; margin:20px 0;">
                We received a request to reset your password for your <strong>mNews</strong> account.
            </p>

            <p style="color:#333; line-height:1.6; margin:20px 0;">
                Click the button below to create a new password:
            </p>

            <table cellpadding="0" cellspacing="0" style="margin:30px 0;">
                <tr>
                    <td style="padding:14px 28px; background-color:#0073e6; border-radius:5px;">
                        <a href="{reset_link}" style="color:#ffffff; text-decoration:none; font-weight:bold; font-size:16px; display:block;">
                            🔒 Reset My Password
                        </a>
                    </td>
                </tr>
            </table>

            <p style="color:#666; font-size:14px; line-height:1.6; margin:20px 0;">
                <strong>Note:</strong> This link will expire in <strong>1 hour</strong> for security reasons.
            </p>

            <p style="color:#333; line-height:1.6; margin:20px 0;">
                If the button doesn't work, copy and paste this link into your browser:
            </p>

            <p style="color:#0073e6; word-break:break-all; font-size:13px; background-color:#f8f8f8; padding:10px; border-radius:4px;">
                {reset_link}
            </p>

            <hr style="margin:30px 0; border:none; border-top:1px solid #ddd;" />

            <p style="font-size:12px; color:#777; line-height:1.4;">
                If you did not request a password reset, please ignore this email. 
                Your password will remain unchanged.
            </p>

            <p style="font-size:12px; color:#777; line-height:1.4;">
                This email was sent to {email} in response to a password reset request.
            </p>
        </div>
    </body>
    </html>
    """

    try:
        msg = EmailMultiAlternatives(subject, text_message, from_email, recipient_list)
        msg.attach_alternative(html_message, "text/html")
        msg.send(fail_silently=False)
        return True
    except Exception as e:
        return False

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
