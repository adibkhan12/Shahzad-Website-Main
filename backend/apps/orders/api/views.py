from rest_framework import mixins, permissions, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.orders.models import Order

from .serializers import OrderSerializer, OrderTrackSerializer


class OrderViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    serializer_class = OrderSerializer
    lookup_field = "reference"

    def get_permissions(self):
        if self.action == "track":
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Order.objects.filter(user=self.request.user)
        return Order.objects.none()

    @action(detail=False, methods=["post"], permission_classes=[permissions.AllowAny])
    def track(self, request):
        ser = OrderTrackSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        order = Order.objects.filter(
            reference=ser.validated_data["reference"],
            email__iexact=ser.validated_data["email"],
        ).first()
        if order is None:
            return Response({"detail": "No order matches that reference and email."}, status=404)
        return Response(OrderSerializer(order).data)
