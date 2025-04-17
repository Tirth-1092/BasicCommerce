from rest_framework import viewsets, permissions
from .models import ShippingAddress, ShippingMethod, DeliveryStatus
from .serializers import (ShippingAddressSerializer,
                         ShippingMethodSerializer,
                         DeliveryStatusSerializer)
from .permissions import IsAddressOwner, IsAdminOrReadOnly

class ShippingAddressViewSet(viewsets.ModelViewSet):
    serializer_class = ShippingAddressSerializer
    permission_classes = [permissions.IsAuthenticated, IsAddressOwner]

    def get_queryset(self):
        return ShippingAddress.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class ShippingMethodViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ShippingMethod.objects.filter(is_active=True)
    serializer_class = ShippingMethodSerializer
    permission_classes = [permissions.AllowAny]

class DeliveryStatusViewSet(viewsets.ModelViewSet):
    serializer_class = DeliveryStatusSerializer
    permission_classes = [permissions.IsAdminUser]
    queryset = DeliveryStatus.objects.all()

class TrackOrderViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = DeliveryStatusSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return DeliveryStatus.objects.filter(
            order__user=self.request.user
        )
