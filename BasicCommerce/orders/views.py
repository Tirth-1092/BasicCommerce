from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from .models import Order, OrderItem
from .serializers import OrderSerializer
from cart.models import Cart#, CartItem
from .permissions import IsOrderOwner, CanCancelOrder
from .pagination import OrderPagination
from .filters import OrderFilter
from .throttling import OrderThrottle
from django_filters.rest_framework import DjangoFilterBackend
from promotions.models import Coupon  # orders/views.py

class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated, IsOrderOwner]
    pagination_class = OrderPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = OrderFilter
    throttle_classes = [OrderThrottle]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)  # Automatically set the creator of the order

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

    @action(detail=False, methods=['post'])
    def checkout(self, request):
        cart = Cart.objects.filter(user=request.user).first()

        if not cart or not cart.items.exists():
            return Response(
                {'error': 'Cart is empty'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Create a new order for the user.
        order = Order.objects.create(user=request.user)

        # Create OrderItems for each CartItem.
        for cart_item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                product=cart_item.product,
                quantity=cart_item.quantity,
                price=cart_item.product.price
            )

        # Clear the cart.
        cart.items.all().delete()

        # Return the order data; the serializer will compute "total" dynamically.
        return Response(
            OrderSerializer(order, context={'request': request}).data,
            status=status.HTTP_201_CREATED
        )

    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        order = self.get_object()

        if not CanCancelOrder().has_object_permission(request, self, order):
            return Response(
                {'error': 'Order cannot be cancelled at this stage'},
                status=status.HTTP_400_BAD_REQUEST
            )

        order.status = 'cancelled'
        order.save()
        return Response(OrderSerializer(order).data)

# orders/views.py

def apply_coupon(order, coupon_code):
    try:
        coupon = Coupon.objects.get(code=coupon_code)
        if coupon.is_valid(order.user, order.total):
            # Apply discount logic
            coupon.used_count += 1
            coupon.save()
            coupon.users.add(order.user)
            return True
    except Coupon.DoesNotExist:
        pass
    return False



