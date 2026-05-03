"""
Send a test email to verify the email pipeline.

In dev (console backend) the email body prints to the runserver terminal.
In prod (SMTP backend, e.g. Resend) it actually sends and you can check
the provider's dashboard for delivery status.

Usage:
    python manage.py send_test_email someone@example.com
    python manage.py send_test_email someone@example.com --subject "Custom"
"""

from django.conf import settings
from django.core.mail import send_mail
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = "Send a test email to confirm the email pipeline works."

    def add_arguments(self, parser):
        parser.add_argument("recipient", help="Email address to send to.")
        parser.add_argument(
            "--subject",
            default="Shahzad Mobile email pipeline test",
            help="Custom subject line.",
        )

    def handle(self, *args, **options):
        recipient = options["recipient"]
        subject = options["subject"]
        body = (
            "This is a test email from Shahzad Mobile.\n\n"
            "If you received this in your inbox, your email pipeline works.\n\n"
            f"Backend: {settings.EMAIL_BACKEND}\n"
            f"From:    {settings.DEFAULT_FROM_EMAIL}\n"
        )

        self.stdout.write(f"Sending to {recipient} via {settings.EMAIL_BACKEND} ...")

        try:
            sent = send_mail(
                subject=subject,
                message=body,
                from_email=None,  # uses DEFAULT_FROM_EMAIL
                recipient_list=[recipient],
                fail_silently=False,
            )
        except Exception as exc:
            raise CommandError(f"Email send failed: {exc}") from exc

        if not sent:
            self.stdout.write(self.style.WARNING("Send returned 0 — nothing was sent."))
            return

        self.stdout.write(self.style.SUCCESS(f"OK: SMTP server accepted {sent} message(s)."))
        if "console" in settings.EMAIL_BACKEND:
            self.stdout.write(
                "(Dev console backend — the email printed above instead of being sent for real.)"
            )
        else:
            self.stdout.write("Check the recipient's inbox and spam folder.")
            if "smtp.resend.com" in getattr(settings, "EMAIL_HOST", ""):
                self.stdout.write("Also visit https://resend.com/emails for delivery status.")
