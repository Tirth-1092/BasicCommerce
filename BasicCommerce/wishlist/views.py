# from rest_framework import viewsets, status
# from rest_framework.response import Response
# from rest_framework.decorators import action
# from rest_framework.permissions import IsAuthenticated
# from .models import Wishlist
# from .serializers import WishlistSerializer, WishlistItemSerializer
# from .permissions import IsWishlistOwner
# from catalog.models import Product

# class WishlistViewSet(viewsets.ModelViewSet):
#     serializer_class = WishlistSerializer
#     permission_classes = [IsAuthenticated, IsWishlistOwner]


#     def perform_create(self, serializer):
#         serializer.save(user=self.request.user)

#     def get_queryset(self):
#         return Wishlist.objects.filter(user=self.request.user)

#     @action(detail=False, methods=['post'])
#     def add(self, request):
#         serializer = WishlistItemSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)

#         wishlist = self.get_queryset().first()
#         product = Product.objects.get(id=serializer.validated_data['product_id'])
#         wishlist.products.add(product)
#         # In WishlistViewSet.add()
#         if wishlist.products.filter(id=product.id).exists():
#             return Response({'error': 'Product already in wishlist'},
#                         status=status.HTTP_400_BAD_REQUEST)


#         return Response(self.get_serializer(wishlist).data,
#                       status=status.HTTP_201_CREATED)

#     @action(detail=False, methods=['delete'])
#     def remove(self, request):
#         serializer = WishlistItemSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)

#         wishlist = self.get_queryset().first()
#         product = Product.objects.get(id=serializer.validated_data['product_id'])
#         wishlist.products.remove(product)

#         return Response(status=status.HTTP_204_NO_CONTENT)
    
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from .models import Wishlist
from .serializers import WishlistSerializer, WishlistItemSerializer
from .permissions import IsWishlistOwner
from catalog.models import Product

class WishlistViewSet(viewsets.ModelViewSet):
    serializer_class = WishlistSerializer
    permission_classes = [IsAuthenticated, IsWishlistOwner]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        # Return the wishlist(s) belonging to the authenticated user.
        return Wishlist.objects.filter(user=self.request.user)

    @action(detail=False, methods=['post'])
    def add(self, request):
        """
        Adds a product to the user's wishlist.
        Expects a payload with 'product_id'.
        If the wishlist does not exist, it is created.
        If the product is already in the wishlist, returns an error.
        """
        serializer = WishlistItemSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        product_id = serializer.validated_data['product_id']

        # Get or create a wishlist for the user.
        wishlist = self.get_queryset()#.first()
        if not wishlist:
            wishlist = Wishlist.objects.create(user=request.user)

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({'error': 'Product not found.'}, status=status.HTTP_404_NOT_FOUND)

        # Check if the product is already in the wishlist.
        if wishlist.products.filter(id=product.id).exists():
            return Response({'error': 'Product already in wishlist'},
                            status=status.HTTP_400_BAD_REQUEST)

        # Add the product to the wishlist.
        wishlist.products.add(product)
        return Response(self.get_serializer(wishlist).data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['delete'])
    def remove(self, request):
        """
        Removes a product from the user's wishlist.
        Expects a payload with 'product_id'.
        """
        serializer = WishlistItemSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        product_id = serializer.validated_data['product_id']

        wishlist = self.get_queryset().first()
        if not wishlist:
            return Response({'error': 'Wishlist not found.'}, status=status.HTTP_404_NOT_FOUND)

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({'error': 'Product not found.'}, status=status.HTTP_404_NOT_FOUND)

        # Check if the product is in the wishlist.
        if not wishlist.products.filter(id=product.id).exists():
            return Response({'error': 'Product not in wishlist.'}, status=status.HTTP_400_BAD_REQUEST)

        wishlist.products.remove(product)
        return Response(status=status.HTTP_204_NO_CONTENT)
