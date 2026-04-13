from allauth.account.signals import user_logged_in
from django.dispatch import receiver

from .services import merge_guest_cart_into_user


@receiver(user_logged_in)
def merge_cart_on_login(sender, request, user, **kwargs):
    sk = request.session.session_key
    merge_guest_cart_into_user(user, sk)
