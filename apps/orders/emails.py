from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string


def send_order_confirmation(order):
    if not order.email:
        return
    ctx = {"order": order, "SITE_URL": settings.SITE_URL, "CURRENCY": order.currency}
    subject = f"Order confirmation — #{order.short_ref}"
    text_body = render_to_string("orders/email/confirmation.txt", ctx)
    html_body = render_to_string("orders/email/confirmation.html", ctx)
    msg = EmailMultiAlternatives(subject, text_body, settings.DEFAULT_FROM_EMAIL, [order.email])
    msg.attach_alternative(html_body, "text/html")
    msg.send(fail_silently=True)
