from rest_framework import serializers
from .models import ShippingAddress, ShippingMethod, DeliveryStatus

class ShippingAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShippingAddress
        fields = ['id', 'street', 'city', 'state',
                 'postal_code', 'country', 'is_primary']
        read_only_fields = ['id', 'user']

class ShippingMethodSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShippingMethod
        fields = ['id', 'name', 'description',
                 'cost', 'estimated_delivery']
        read_only_fields = ['id']

class DeliveryStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeliveryStatus
        fields = ['status', 'tracking_number',
                 'carrier', 'last_updated']
        read_only_fields = ['last_updated']
