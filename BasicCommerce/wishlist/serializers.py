from rest_framework import serializers
from .models import Wishlist
from catalog.serializers import ProductSerializer  # Import from catalog app

class WishlistSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True, read_only=True)

    class Meta:
        model = Wishlist
        fields = ['id', 'products', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

class WishlistItemSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
