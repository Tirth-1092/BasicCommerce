from django_filters import rest_framework as filters
from .models import Order

class OrderFilter(filters.FilterSet):
    status = filters.CharFilter(lookup_expr='iexact')
    min_total = filters.NumberFilter(field_name='total', lookup_expr='gte')
    max_total = filters.NumberFilter(field_name='total', lookup_expr='lte')

    class Meta:
        model = Order
        fields = ['status', 'min_total', 'max_total']
