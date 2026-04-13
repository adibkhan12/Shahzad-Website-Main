from django.shortcuts import get_object_or_404, redirect, render

from .forms import RepairBookingForm
from .models import RepairBooking, RepairService


def services(request):
    device = request.GET.get("device", "").strip()
    qs = RepairService.objects.all()
    if device:
        qs = qs.filter(device=device)
    featured = RepairService.objects.filter(is_featured=True)[:4]
    return render(
        request,
        "repairs/services.html",
        {
            "services": qs,
            "featured": featured,
            "current_device": device,
            "device_choices": RepairService.Device.choices,
        },
    )


def book(request, slug=None):
    service = get_object_or_404(RepairService, slug=slug) if slug else None

    if request.method == "POST":
        form = RepairBookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.service = service
            booking.save()
            return redirect("repairs:confirm", reference=booking.reference)
    else:
        initial = {}
        if request.user.is_authenticated:
            initial["email"] = request.user.email
            initial["name"] = (request.user.get_full_name() or "").strip() or request.user.email.split("@")[0]
        form = RepairBookingForm(initial=initial)

    return render(request, "repairs/book.html", {"form": form, "service": service})


def confirm(request, reference):
    booking = get_object_or_404(RepairBooking, reference=reference)
    return render(request, "repairs/confirm.html", {"booking": booking})


def status(request):
    reference = request.GET.get("ref", "").strip()
    phone = request.GET.get("phone", "").strip()
    booking = None
    error = None
    if reference and phone:
        try:
            booking = RepairBooking.objects.get(reference=reference, phone=phone)
        except (RepairBooking.DoesNotExist, ValueError):
            error = "No booking matches that reference and phone."
    return render(request, "repairs/status.html", {
        "booking": booking, "error": error, "reference": reference, "phone": phone,
    })
