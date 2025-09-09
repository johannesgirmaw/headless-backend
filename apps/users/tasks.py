"""
Email service for user verification and notifications.
"""

from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from celery import shared_task
from apps.users.models import User
from apps.accounts.models import Account
from apps.organizations.models import Organization
import logging

logger = logging.getLogger(__name__)


@shared_task
def send_email_verification(user_id, verification_token):
    """
    Send email verification to user.
    """
    try:
        user = User.objects.get(id=user_id)

        # Create verification URL
        verification_url = f"{settings.FRONTEND_URL}/verify-email?token={verification_token}"

        # Render email template
        context = {
            'user': user,
            'verification_url': verification_url,
            'site_name': 'Headless SaaS Platform',
        }

        subject = 'Verify Your Email Address'
        html_message = render_to_string(
            'emails/email_verification.html', context)
        plain_message = render_to_string(
            'emails/email_verification.txt', context)

        send_mail(
            subject=subject,
            message=plain_message,
            html_message=html_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=False,
        )

        logger.info(f"Email verification sent to {user.email}")
        return True

    except User.DoesNotExist:
        logger.error(f"User with id {user_id} not found")
        return False
    except Exception as e:
        logger.error(f"Failed to send email verification: {str(e)}")
        return False


@shared_task
def send_password_reset_email(user_id, reset_token):
    """
    Send password reset email to user.
    """
    try:
        user = User.objects.get(id=user_id)

        # Create reset URL
        reset_url = f"{settings.FRONTEND_URL}/reset-password?token={reset_token}"

        # Render email template
        context = {
            'user': user,
            'reset_url': reset_url,
            'site_name': 'Headless SaaS Platform',
        }

        subject = 'Reset Your Password'
        html_message = render_to_string('emails/password_reset.html', context)
        plain_message = render_to_string('emails/password_reset.txt', context)

        send_mail(
            subject=subject,
            message=plain_message,
            html_message=html_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=False,
        )

        logger.info(f"Password reset email sent to {user.email}")
        return True

    except User.DoesNotExist:
        logger.error(f"User with id {user_id} not found")
        return False
    except Exception as e:
        logger.error(f"Failed to send password reset email: {str(e)}")
        return False


@shared_task
def send_welcome_email(user_id):
    """
    Send welcome email to new user.
    """
    try:
        user = User.objects.get(id=user_id)

        # Render email template
        context = {
            'user': user,
            'site_name': 'Headless SaaS Platform',
            'login_url': f"{settings.FRONTEND_URL}/login",
        }

        subject = 'Welcome to Headless SaaS Platform'
        html_message = render_to_string('emails/welcome.html', context)
        plain_message = render_to_string('emails/welcome.txt', context)

        send_mail(
            subject=subject,
            message=plain_message,
            html_message=html_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=False,
        )

        logger.info(f"Welcome email sent to {user.email}")
        return True

    except User.DoesNotExist:
        logger.error(f"User with id {user_id} not found")
        return False
    except Exception as e:
        logger.error(f"Failed to send welcome email: {str(e)}")
        return False


@shared_task
def send_organization_invitation_email(user_id, organization_id, invitation_token):
    """
    Send organization invitation email to user.
    """
    try:
        user = User.objects.get(id=user_id)
        organization = Organization.objects.get(id=organization_id)

        # Create invitation URL
        invitation_url = f"{settings.FRONTEND_URL}/accept-invitation?token={invitation_token}"

        # Render email template
        context = {
            'user': user,
            'organization': organization,
            'invitation_url': invitation_url,
            'site_name': 'Headless SaaS Platform',
        }

        subject = f'Invitation to join {organization.name}'
        html_message = render_to_string(
            'emails/organization_invitation.html', context)
        plain_message = render_to_string(
            'emails/organization_invitation.txt', context)

        send_mail(
            subject=subject,
            message=plain_message,
            html_message=html_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=False,
        )

        logger.info(f"Organization invitation sent to {user.email}")
        return True

    except (User.DoesNotExist, Organization.DoesNotExist) as e:
        logger.error(f"User or Organization not found: {str(e)}")
        return False
    except Exception as e:
        logger.error(f"Failed to send organization invitation: {str(e)}")
        return False


@shared_task
def send_account_notification_email(account_id, notification_type, data):
    """
    Send account-related notification emails.
    """
    try:
        account = Account.objects.get(id=account_id)

        # Get account administrators
        admins = User.objects.filter(
            account=account,
            is_account_admin=True,
            is_active=True
        )

        if not admins.exists():
            logger.warning(
                f"No active account administrators found for account {account_id}")
            return False

        # Render email template based on notification type
        context = {
            'account': account,
            'site_name': 'Headless SaaS Platform',
            'data': data,
        }

        if notification_type == 'subscription_expiring':
            subject = f'Subscription Expiring Soon - {account.company_name}'
            html_template = 'emails/subscription_expiring.html'
            text_template = 'emails/subscription_expiring.txt'
        elif notification_type == 'subscription_expired':
            subject = f'Subscription Expired - {account.company_name}'
            html_template = 'emails/subscription_expired.html'
            text_template = 'emails/subscription_expired.txt'
        elif notification_type == 'usage_limit_warning':
            subject = f'Usage Limit Warning - {account.company_name}'
            html_template = 'emails/usage_limit_warning.html'
            text_template = 'emails/usage_limit_warning.txt'
        else:
            logger.error(f"Unknown notification type: {notification_type}")
            return False

        html_message = render_to_string(html_template, context)
        plain_message = render_to_string(text_template, context)

        # Send to all account administrators
        recipient_list = [admin.email for admin in admins]

        send_mail(
            subject=subject,
            message=plain_message,
            html_message=html_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=recipient_list,
            fail_silently=False,
        )

        logger.info(
            f"Account notification '{notification_type}' sent to {len(recipient_list)} administrators")
        return True

    except Account.DoesNotExist:
        logger.error(f"Account with id {account_id} not found")
        return False
    except Exception as e:
        logger.error(f"Failed to send account notification: {str(e)}")
        return False


@shared_task
def send_email_verification_reminders():
    """
    Send reminders to users who haven't verified their email.
    """
    try:
        unverified_users = User.objects.filter(
            is_verified=False,
            is_active=True
        )

        for user in unverified_users:
            # Generate new verification token
            verification_token = user.generate_verification_token()

            # Send reminder email
            send_email_verification.delay(user.id, verification_token)

        logger.info(
            f"Email verification reminders sent to {unverified_users.count()} users")
        return True

    except Exception as e:
        logger.error(f"Failed to send email verification reminders: {str(e)}")
        return False


@shared_task
def cleanup_expired_tokens():
    """
    Clean up expired JWT tokens from blacklist.
    """
    try:
        from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken, OutstandingToken

        # Delete expired blacklisted tokens
        expired_blacklisted = BlacklistedToken.objects.filter(
            token__expires_at__lt=timezone.now()
        )
        expired_count = expired_blacklisted.count()
        expired_blacklisted.delete()

        # Delete expired outstanding tokens
        expired_outstanding = OutstandingToken.objects.filter(
            expires_at__lt=timezone.now()
        )
        outstanding_count = expired_outstanding.count()
        expired_outstanding.delete()

        logger.info(
            f"Cleaned up {expired_count} expired blacklisted tokens and {outstanding_count} expired outstanding tokens")
        return True

    except Exception as e:
        logger.error(f"Failed to cleanup expired tokens: {str(e)}")
        return False
