from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny,IsAuthenticated
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.authentication import JWTAuthentication
from .serializers import CustomRegistrationSerializer, UserProfileSerializer

# from rest_framework.decorators import action
# from rest_framework_simplejwt.tokens import RefreshToken


User = get_user_model()
#
# class AuthViewSet(viewsets.ViewSet):
#     permission_classes = [AllowAny]
#
#     # User Registration (No Token, Uses Djoser's Login)
#     @action(detail=False, methods=['post'])
#     def register(self, request):
#         serializer = CustomRegistrationSerializer(data=request.data)
#         if serializer.is_valid():
#             user = serializer.save()  # Create user
#             return Response(
#                 {
#                     "message": "User registered successfully",
#                     "user": serializer.data
#                 },
#                 status=status.HTTP_201_CREATED
#             )
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RegistrationViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = CustomRegistrationSerializer
    permission_classes = [AllowAny]
    http_method_names = ['post']  # Only allow POST requests (registration)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()  # Create user
            return Response(
                {
                    "message": "User registered successfully",
                    "user": serializer.data
                },
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#
# class AuthViewSet(viewsets.ViewSet):
#     permission_classes = [AllowAny]
#
#     # User Registration
#     @action(detail=False, methods=['post'])
#     def register(self, request):
#         serializer = CustomRegistrationSerializer(data=request.data)
#
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     # User Login
#     @action(detail=False, methods=['post'])
#     def login(self, request):
#         serializer = LoginSerializer(data=request.data)
#         if serializer.is_valid():
#             # user = serializer.save()
#             refresh = RefreshToken.for_user(user)
#             return Response(
#                 {
#                     "message": "User registered successfully",
#                     "user": LoginSerializer(user).data,
#                     "access": str(refresh.access_token),
#                     "refresh": str(refresh)
#                 },
#                 status=status.HTTP_201_CREATED
#             )
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#

class UserProfileViewSet(viewsets.ModelViewSet):
    serializer_class = UserProfileSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user  # Retrieve the authenticated user

    def list(self, request, *args, **kwargs):
        """ Restrict listing, return only the current user's profile. """
        serializer = self.get_serializer(self.get_object())
        return Response(serializer.data)




  