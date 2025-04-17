from django_filters import rest_framework as filters
from .models import Payment

class PaymentFilter(filters.FilterSet):
    status = filters.CharFilter(lookup_expr='iexact')
    min_amount = filters.NumberFilter(field_name='amount', lookup_expr='gte')
    max_amount = filters.NumberFilter(field_name='amount', lookup_expr='lte')

    class Meta:
        model = Payment
        fields = ['status', 'min_amount', 'max_amount']

