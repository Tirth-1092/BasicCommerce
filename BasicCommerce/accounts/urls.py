#from django.contrib import admin
from django.urls import path, include
#from django.urls import re_path  # Import re_path for compatibility
from .views import RegistrationViewSet,UserProfileViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'auth', RegistrationViewSet, basename='auth')
router.register(r'profile', UserProfileViewSet, basename='user-profile')




urlpatterns = [

    path('', include(router.urls)),  # This includes /auth/register/
    path('auth/', include('djoser.urls')),  # Includes default Djoser endpoints
    path('auth/', include('djoser.urls.jwt')),  # Includes JWT login/logout endpoints
    # path('profile/', UserProfileView.as_view(), name='user-profile'),
    
]

