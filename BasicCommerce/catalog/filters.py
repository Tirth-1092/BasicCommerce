from django_filters import rest_framework as filters
from .models import Product,Category

class ProductFilter(filters.FilterSet):
    min_price = filters.NumberFilter(field_name='price', lookup_expr='gte')
    max_price = filters.NumberFilter(field_name='price', lookup_expr='lte')
    category = filters.CharFilter(field_name='category', lookup_expr='icontains')

    class Meta:
        model = Product
        fields = ['category', 'min_price', 'max_price']



class CategoryFilter(filters.FilterSet):
    name = filters.CharFilter(field_name='name',lookup_expr='icontains')
    parent = filters.NumberFilter(field_name='parent__id')

    class Meta:
        model = Category
        fields = ['name', 'parent']