from rest_framework import viewsets,filters
from .models import Category, Product, Review
from .serializers import CategorySerializer, ProductSerializer, ReviewSerializer
from .permissions import IsAdminOrReadOnly, IsAdminOrSeller, IsReviewOwnerOrReadOnly
from .filters import ProductFilter,CategoryFilter
from .pagination import CategoryPagination
from rest_framework_simplejwt.authentication import JWTAuthentication
from django_filters.rest_framework import DjangoFilterBackend
from .throttling import CategoryThrottle
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from .pagination import ProductPagination


class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    pagination_class = CategoryPagination
    permission_classes = [IsAdminOrReadOnly]  # Only admins can manage categories
    authentication_classes = [JWTAuthentication]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_class = CategoryFilter
    search_fields = ['name']
    throttle_classes = [CategoryThrottle]


    def get_queryset(self):
        # For list action, allow filtering to only top-level categories (or by parent if provided)
        if self.action == 'list':
            parent_id = self.request.query_params.get('parent')
            if parent_id:
                return Category.objects.filter(parent_id=parent_id)
            return Category.objects.filter(parent__isnull=True)
        # For retrieve, update, destroy, etc., return all categories.
        return Category.objects.all()
    
   

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all().order_by('-created_at')
    serializer_class = ProductSerializer
    pagination_class = ProductPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_class = ProductFilter
    search_fields = ['name', 'description']
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAdminOrSeller]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)  # Automatically set the creator of the product
        
    def get_queryset(self):
        """Filter products based on the authenticated user's role."""
        if self.request.user.role == 'seller':
            return Product.objects.filter(created_by=self.request.user).order_by('-created_at')
        return Product.objects.all().order_by('-created_at')


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all().order_by('-created_at')
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated, IsReviewOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
