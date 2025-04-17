from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (ShippingAddressViewSet,
                   ShippingMethodViewSet,
                   DeliveryStatusViewSet,
                   TrackOrderViewSet)

router = DefaultRouter()
router.register(r'addresses', ShippingAddressViewSet, basename='address')
router.register(r'methods', ShippingMethodViewSet, basename='method')
router.register(r'deliveries', DeliveryStatusViewSet, basename='delivery')
router.register(r'track', TrackOrderViewSet, basename='track')

urlpatterns = [
    path('', include(router.urls)),
]
