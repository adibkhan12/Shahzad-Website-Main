from django.db import transaction
from uuid import UUID

from .models import Cart, CartItem


def _ensure_session(request):
    if not request.session.session_key:
        request.session.save()
    return request.session.session_key


def get_or_create_cart(request) -> Cart:
    if request.user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(user=request.user)
        return cart
    sk = _ensure_session(request)
    cart, _ = Cart.objects.get_or_create(session_key=sk)
    return cart


def normalize_guest_session_key(session_key: str | None) -> str:
    if not session_key:
        return ""
    session_key = str(session_key).strip()
    if len(session_key) > 64:
        return ""
    try:
        return str(UUID(session_key))
    except (TypeError, ValueError, AttributeError):
        return ""


@transaction.atomic
def merge_guest_cart_into_user(user, session_key: str):
    session_key = normalize_guest_session_key(session_key)
    if not session_key:
        return
    try:
        guest = Cart.objects.select_for_update().get(session_key=session_key, user__isnull=True)
    except Cart.DoesNotExist:
        return
    user_cart, _ = Cart.objects.get_or_create(user=user)
    for gi in guest.items.all():
        ui, created = CartItem.objects.get_or_create(
            cart=user_cart, product=gi.product, defaults={"quantity": gi.quantity}
        )
        if not created:
            ui.quantity = ui.quantity + gi.quantity
            ui.save(update_fields=["quantity"])
    guest.delete()
