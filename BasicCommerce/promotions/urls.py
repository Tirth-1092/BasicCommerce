from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CouponViewSet, DiscountViewSet, AvailableDiscountsViewSet

router = DefaultRouter()
router.register(r'coupons', CouponViewSet)
router.register(r'discounts', DiscountViewSet)

urlpatterns = [
    path('available/', AvailableDiscountsViewSet.as_view({'get': 'list'}), name='available-discounts'),
    path('', include(router.urls)),
]
