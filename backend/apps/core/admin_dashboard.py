from datetime import timedelta
from decimal import Decimal

from django.db.models import Count, F, Sum
from django.utils import timezone


def _pct_change(current, previous):
    if previous in (0, None):
        return None
    try:
        return round(((float(current) - float(previous)) / float(previous)) * 100, 1)
    except Exception:
        return None


def dashboard_callback(request, context):
    """Shahzad admin dashboard: KPIs with trends, 14-day revenue sparkline,
    top sellers, recent activity feed, low-stock alerts, quick-add actions."""
    from apps.accounts.models import User
    from apps.catalog.models import Product
    from apps.orders.models import Order, OrderItem
    from apps.repairs.models import RepairBooking

    now = timezone.now()
    day_ago = now - timedelta(days=1)
    two_days_ago = now - timedelta(days=2)
    week_ago = now - timedelta(days=7)
    two_weeks_ago = now - timedelta(days=14)
    month_ago = now - timedelta(days=30)
    two_months_ago = now - timedelta(days=60)

    orders_today = Order.objects.filter(created_at__gte=day_ago).count()
    orders_yesterday = Order.objects.filter(
        created_at__gte=two_days_ago, created_at__lt=day_ago
    ).count()
    orders_week = Order.objects.filter(created_at__gte=week_ago).count()
    orders_prev_week = Order.objects.filter(
        created_at__gte=two_weeks_ago, created_at__lt=week_ago
    ).count()
    orders_total = Order.objects.count()

    paid_q = Order.objects.filter(paid=True)
    revenue_all = paid_q.aggregate(s=Sum("total"))["s"] or Decimal("0")
    revenue_month = paid_q.filter(created_at__gte=month_ago).aggregate(s=Sum("total"))["s"] or Decimal("0")
    revenue_prev_month = paid_q.filter(
        created_at__gte=two_months_ago, created_at__lt=month_ago
    ).aggregate(s=Sum("total"))["s"] or Decimal("0")

    customers_total = User.objects.filter(is_staff=False).count()
    customers_week = User.objects.filter(is_staff=False, date_joined__gte=week_ago).count()

    product_total = Product.objects.filter(is_active=True).count()
    low_stock = Product.objects.filter(is_active=True, stock__gt=0, stock__lt=5).count()
    out_of_stock = Product.objects.filter(is_active=True, stock=0).count()

    bookings_open = RepairBooking.objects.exclude(
        status__in=["completed", "cancelled"]
    ).count()
    bookings_today = RepairBooking.objects.filter(created_at__gte=day_ago).count()

    # 14-day revenue sparkline
    start = (now - timedelta(days=13)).date()
    rev_rows = (
        paid_q.filter(created_at__date__gte=start)
        .values("created_at__date")
        .annotate(s=Sum("total"))
    )
    rev_by_day = {r["created_at__date"]: float(r["s"] or 0) for r in rev_rows}
    spark = []
    for i in range(14):
        d = start + timedelta(days=i)
        spark.append({"date": d, "value": rev_by_day.get(d, 0.0)})
    max_val = max((p["value"] for p in spark), default=0) or 1
    for p in spark:
        p["height_pct"] = round((p["value"] / max_val) * 100, 1) if max_val else 0

    # Top sellers
    top_rows = (
        OrderItem.objects.filter(
            order__status__in=["paid", "shipped", "delivered"],
            product__isnull=False,
        )
        .values("product_id")
        .annotate(units=Sum("quantity"), revenue=Sum(F("unit_price") * F("quantity")))
        .order_by("-units")[:5]
    )
    top_ids = [r["product_id"] for r in top_rows]
    prods_by_id = {p.id: p for p in Product.objects.filter(id__in=top_ids).select_related("brand")}
    top_sellers = []
    for r in top_rows:
        p = prods_by_id.get(r["product_id"])
        if not p:
            continue
        top_sellers.append({
            "id": p.id,
            "title": p.title,
            "brand": p.brand.name if p.brand else "—",
            "image": p.primary_image,
            "units": r["units"],
            "revenue": r["revenue"] or 0,
        })

    low_stock_rows = (
        Product.objects.filter(is_active=True, stock__lt=5)
        .select_related("brand", "category")
        .order_by("stock", "title")[:6]
    )

    status_breakdown = list(
        Order.objects.values("status").annotate(n=Count("id")).order_by("-n")
    )

    recent_orders = (
        Order.objects.select_related("user").order_by("-created_at")[:6]
    )

    activity = []
    for o in Order.objects.order_by("-created_at")[:8]:
        activity.append({
            "icon": "🛒",
            "title": f"Order {o.short_ref} · {o.total} {o.currency}",
            "sub": f"{o.name} · {o.get_status_display()}",
            "at": o.created_at,
            "link": f"/admin/orders/order/{o.id}/change/",
        })
    for b in RepairBooking.objects.order_by("-created_at")[:5]:
        activity.append({
            "icon": "🔧",
            "title": f"Repair {b.short_ref} · {b.device_brand} {b.device_model}",
            "sub": f"{b.name} · {b.get_status_display()}",
            "at": b.created_at,
            "link": f"/admin/repairs/repairbooking/{b.id}/change/",
        })
    for u in User.objects.filter(is_staff=False).order_by("-date_joined")[:3]:
        activity.append({
            "icon": "👤",
            "title": f"New customer · {u.email}",
            "sub": (u.get_full_name() or "").strip() or "—",
            "at": u.date_joined,
            "link": f"/admin/accounts/user/{u.id}/change/",
        })
    activity.sort(key=lambda x: x["at"], reverse=True)
    activity = activity[:8]

    context.update({
        "kpis": [
            {
                "label": "Orders today",
                "value": orders_today,
                "hint": f"{orders_yesterday} yesterday",
                "trend": _pct_change(orders_today, orders_yesterday),
                "icon": "🛒",
                "accent": "#0EA5E9",
            },
            {
                "label": "Revenue (30d)",
                "value": f"{revenue_month:,.0f} AED",
                "hint": f"{revenue_all:,.0f} all-time",
                "trend": _pct_change(revenue_month, revenue_prev_month),
                "icon": "💰",
                "accent": "#10B981",
            },
            {
                "label": "Active products",
                "value": product_total,
                "hint": f"{low_stock} low · {out_of_stock} out",
                "trend": None,
                "icon": "📦",
                "accent": "#740DC2",
            },
            {
                "label": "Open repairs",
                "value": bookings_open,
                "hint": f"{bookings_today} new today",
                "trend": None,
                "icon": "🔧",
                "accent": "#F59E0B",
            },
        ],
        "week_kpis": [
            {"label": "Orders (7d)", "value": orders_week, "trend": _pct_change(orders_week, orders_prev_week)},
            {"label": "New customers (7d)", "value": customers_week},
            {"label": "Customers total", "value": customers_total},
        ],
        "sparkline": spark,
        "top_sellers": top_sellers,
        "low_stock_rows": low_stock_rows,
        "order_status_breakdown": status_breakdown,
        "recent_orders": recent_orders,
        "activity": activity,
        "orders_total": orders_total,
        "quick_adds": [
            {"label": "Add product", "link": "/admin/catalog/product/add/", "icon": "📦"},
            {"label": "Add category", "link": "/admin/catalog/category/add/", "icon": "🗂️"},
            {"label": "Add brand", "link": "/admin/catalog/brand/add/", "icon": "🏷️"},
            {"label": "Add banner", "link": "/admin/catalog/adbanner/add/", "icon": "🎯"},
            {"label": "Add repair service", "link": "/admin/repairs/repairservice/add/", "icon": "🛠️"},
        ],
    })
    return context
