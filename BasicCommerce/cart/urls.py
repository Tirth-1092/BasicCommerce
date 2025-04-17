# from django.urls import path, include
# from rest_framework.routers import DefaultRouter
# from .views import CartViewSet

# router = DefaultRouter()
# router.register(r'', CartViewSet, basename='cart')

# urlpatterns = [
#     path('', include(router.urls)),
# ]
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CartViewSet

router = DefaultRouter()
router.register(r'', CartViewSet, basename='cart')

urlpatterns = [
    path('', include(router.urls)),
]
  