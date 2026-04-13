from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render

from .models import Order


@login_required
def order_list(request):
    orders = request.user.orders.all()
    return render(request, "orders/list.html", {"orders": orders})


def order_detail(request, reference):
    order = get_object_or_404(Order, reference=reference)
    # public page accessed via reference UUID; owner-only if authenticated mismatch
    if order.user and request.user.is_authenticated and order.user_id != request.user.id:
        if not request.user.is_staff:
            return render(request, "orders/detail.html", {"order": None, "forbidden": True}, status=403)
    return render(request, "orders/detail.html", {"order": order})


def track(request):
    reference = request.GET.get("ref", "").strip()
    email = request.GET.get("email", "").strip()
    order = None
    error = None
    if reference and email:
        try:
            order = Order.objects.get(reference=reference, email__iexact=email)
        except Order.DoesNotExist:
            error = "No order matches that reference and email."
    return render(request, "orders/track.html", {"order": order, "error": error, "reference": reference, "email": email})
