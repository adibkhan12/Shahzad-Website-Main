from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def dashboard(request):
    orders = request.user.orders.all()[:20]
    wishlist = request.user.wished_products.select_related("product")[:12]
    addresses = request.user.addresses.all()
    return render(
        request,
        "accounts/dashboard.html",
        {"orders": orders, "wishlist": wishlist, "addresses": addresses},
    )
