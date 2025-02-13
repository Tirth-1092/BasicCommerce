from rest_framework import viewsets
from .models import Category, Product, Review
from .serializers import CategorySerializer, ProductSerializer, ReviewSerializer
from .permissions import IsAdminOrReadOnly, IsSellerOrReadOnly, IsReviewOwnerOrReadOnly
from .filters import ProductFilter
from django_filters import rest_framework as filters

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]  # Only admins can manage categories

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsSellerOrReadOnly]  # Only sellers can manage products
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = ProductFilter

    def perform_create(self, serializer):
        serializer.save(seller=self.request.user)

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsReviewOwnerOrReadOnly]  # Only review owners can edit/delete reviews

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)