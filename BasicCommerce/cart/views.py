# from rest_framework import viewsets, permissions, status
# from rest_framework.response import Response
# from rest_framework.decorators import action
# from .models import Cart, CartItem
# from .serializers import CartSerializer, CartItemSerializer
# from .permissions import IsCartOwner
# from .pagination import CartPagination
# from .filters import CartItemFilter
# from .throttling import CartThrottle
# from django_filters.rest_framework import DjangoFilterBackend


# class CartViewSet(viewsets.ModelViewSet):
#     serializer_class = CartSerializer
#     permission_classes = [permissions.IsAuthenticated, IsCartOwner]
#     pagination_class = CartPagination
#     filter_backends = [DjangoFilterBackend]
#     filterset_class = CartItemFilter
#     throttle_classes = [CartThrottle]

#     def perform_create(self, serializer):
#         serializer.save(user=self.request.user)  # Automatically set the creator of the product

#     def get_queryset(self):
#         return Cart.objects.filter(user=self.request.user)
    

#     @action(detail=False, methods=['post'])
#     def add_item(self, request):
#         cart = self.get_queryset().first()
#         if not cart:
#             cart = Cart.objects.create(user=request.user)
#         product_id = request.data.get('product')
#         quantity = request.data.get('quantity', 1)
#         cart_item, created = CartItem.objects.get_or_create(
#             cart=cart,
#             product_id=product_id,
#             defaults={'quantity': quantity}
#         )
#         if not created:
#             cart_item.quantity += int(quantity)
#             cart_item.save()
#         return Response(CartItemSerializer(cart_item).data, status=status.HTTP_201_CREATED)

#     @action(detail=False, methods=['put'])
#     def update_item(self, request):
#         cart = self.get_queryset().first()
#         product_id = request.data.get('product')
#         quantity = request.data.get('quantity')
#         cart_item = CartItem.objects.get(cart=cart, product_id=product_id)
#         cart_item.quantity = int(quantity)
#         cart_item.save()
#         return Response(CartItemSerializer(cart_item).data)

#     @action(detail=False, methods=['delete'])
#     def remove_item(self, request):
#         cart = self.get_queryset().first()
#         product_id = request.data.get('product')
#         CartItem.objects.filter(cart=cart, product_id=product_id).delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

#     @action(detail=False, methods=['delete'])
#     def clear_cart(self, request):
#         cart = self.get_queryset().first()
#         cart.items.all().delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from .models import Cart
from .serializers import CartSerializer
from .permissions import IsCartOwner
from .pagination import CartPagination
from .filters import CartItemFilter
from .throttling import CartThrottle

class CartViewSet(viewsets.ModelViewSet):
    serializer_class = CartSerializer
    permission_classes = [permissions.IsAuthenticated, IsCartOwner]
    pagination_class = CartPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = CartItemFilter
    throttle_classes = [CartThrottle]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)
    # def get_queryset(self):
    #     user = self.request.user
    #     return user.art.all()
    
    @action(detail=False, methods=['post'])
    def add_item(self, request):
        cart, created = Cart.objects.get_or_create(
            user=request.user,
            product_id=request.data.get('product'),
            defaults={'quantity': request.data.get('quantity', 1)}
        )
        if not created:
            cart.quantity += int(request.data.get('quantity', 1))
            cart.save()
        return Response(CartSerializer(cart).data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['put'])
    def update_item(self, request):
        cart = self.get_queryset().filter(product_id=request.data.get('product')).first()
        if not cart:
            return Response({"error": "Item not found in cart"}, status=status.HTTP_404_NOT_FOUND)
        cart.quantity = int(request.data.get('quantity'))
        cart.save()
        return Response(CartSerializer(cart).data)

    @action(detail=False, methods=['delete'])
    def remove_item(self, request):
        cart = self.get_queryset().filter(product_id=request.data.get('product')).first()
        if cart:
            cart.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['delete'])
    def clear_cart(self, request):
        self.get_queryset().delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
