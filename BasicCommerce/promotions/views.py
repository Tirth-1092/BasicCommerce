from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from django.utils import timezone  # Added missing import
from .models import Coupon, Discount
from .serializers import CouponSerializer, DiscountSerializer, CouponValidationSerializer

class CouponViewSet(viewsets.ModelViewSet):
    queryset = Coupon.objects.all()
    serializer_class = CouponSerializer
    permission_classes = [IsAdminUser]

    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def validate(self, request):
        serializer = CouponValidationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            coupon = Coupon.objects.get(code=serializer.validated_data['code'])
            if coupon.is_valid(request.user, serializer.validated_data['cart_total']):
                return Response(CouponSerializer(coupon).data)
            return Response({'error': 'Coupon is not valid'}, status=status.HTTP_400_BAD_REQUEST)
        except Coupon.DoesNotExist:
            return Response({'error': 'Invalid coupon code'}, status=status.HTTP_404_NOT_FOUND)

class DiscountViewSet(viewsets.ModelViewSet):
    queryset = Discount.objects.filter(active=True)
    serializer_class = DiscountSerializer
    permission_classes = [IsAdminUser]

class AvailableDiscountsViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = DiscountSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        now = timezone.now()
        return Discount.objects.filter(
            active=True,
            valid_from__lte=now,
            valid_to__gte=now
        )
