# from rest_framework import serializers
# from .models import Payment, PaymentIntent

# class PaymentSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Payment
#         fields = ['id', 'order', 'amount', 'status', 'stripe_payment_id', 'created_at']
#         read_only_fields = ['id', 'status', 'stripe_payment_id', 'created_at']

# class PaymentIntentSerializer(serializers.Serializer):
#     order_id = serializers.IntegerField()
#     currency = serializers.CharField(default='inr')

# from rest_framework import serializers
# from .models import Payment, PaymentIntent

# class PaymentSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Payment
#         fields = ['id', 'order', 'amount', 'status', 'stripe_payment_id', 'created_at']
#         read_only_fields = ['id', 'status', 'stripe_payment_id', 'created_at']

# class PaymentIntentSerializer(serializers.Serializer):
#     order_id = serializers.IntegerField()
#     currency = serializers.CharField(default='inr')

from rest_framework import serializers
from .models import Payment

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['id', 'order', 'amount', 'status', 'created_at']
        # All these fields are set on the server side
        read_only_fields = ['id', 'order', 'amount', 'status', 'stripe_payment_id', 'created_at']

class PaymentIntentSerializer(serializers.Serializer):
    order_id = serializers.IntegerField()
    # Default to 'inr', allow null, not required
    currency = serializers.CharField(default='inr', allow_null=True, required=False)
