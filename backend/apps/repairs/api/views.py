from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.repairs.models import RepairBooking, RepairService

from .serializers import RepairBookingSerializer, RepairServiceSerializer, RepairStatusSerializer


class RepairServiceViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = RepairService.objects.all()
    serializer_class = RepairServiceSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = "slug"
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["device", "is_featured"]

    @action(detail=False, methods=["get"])
    def devices(self, request):
        return Response([{"value": v, "label": lab} for v, lab in RepairService.Device.choices])


class RepairBookingViewSet(viewsets.GenericViewSet):
    serializer_class = RepairBookingSerializer
    queryset = RepairBooking.objects.all()
    permission_classes = [permissions.AllowAny]
    lookup_field = "reference"

    def create(self, request):
        ser = self.get_serializer(data=request.data)
        ser.is_valid(raise_exception=True)
        ser.save()
        return Response(ser.data, status=201)

    def retrieve(self, request, reference=None):
        booking = self.get_object()
        return Response(
            {
                "reference": str(booking.reference),
                "short_ref": booking.short_ref,
                "status": booking.status,
                "created_at": booking.created_at,
            }
        )

    @action(detail=False, methods=["post"])
    def status(self, request):
        ser = RepairStatusSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        booking = RepairBooking.objects.filter(
            reference=ser.validated_data["reference"],
            phone=ser.validated_data["phone"],
        ).first()
        if booking is None:
            return Response({"detail": "No booking matches that reference and phone."}, status=404)
        return Response(self.get_serializer(booking).data)
