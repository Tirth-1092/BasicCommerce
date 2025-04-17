# from rest_framework import serializers
# from .models import Cart, CartItem
# from catalog.models import Product
# class CartItemSerializer(serializers.ModelSerializer):
#     product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())

#     class Meta:
#         model = CartItem
#         fields = ['id', 'product', 'quantity']
#         read_only_fields = ['id']

# class CartSerializer(serializers.ModelSerializer):
#     items = CartItemSerializer(many=True, read_only=False)

#     class Meta:
#         model = Cart
#         fields = ['id', 'user', 'items', 'created_at', 'updated_at']
#         read_only_fields = ['id', 'user', 'created_at', 'updated_at']
from rest_framework import serializers
from .models import Cart
from catalog.models import Product

class CartSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())

    class Meta:
        model = Cart
        fields = ['id', 'user', 'product', 'quantity', 'created_at', 'updated_at']
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']
