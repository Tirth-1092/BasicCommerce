from django_filters import rest_framework as filters
from .models import Cart

class CartItemFilter(filters.FilterSet):
    product = filters.NumberFilter(field_name='product__id')

    class Meta:
        model = Cart
        fields = ['product']
