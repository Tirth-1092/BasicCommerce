from rest_framework import serializers
from djoser.serializers import UserCreateSerializer, UserSerializer
from django.contrib.auth import get_user_model #, authenticate
# from rest_framework_simplejwt.tokens import RefreshToken
from .models import User

User = get_user_model()   # retrieves the project's active User model


class CustomRegistrationSerializer(UserCreateSerializer):
    confirm_password = serializers.CharField(write_only=True,style={'input_type': 'password'}  # 👈 This makes it a password field
    )

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'confirm_password', 'phone_number', 'role']
        extra_kwargs = {'password': {'write_only': True, 'style': {'input_type': 'password'}}}  # 👈 Mask password too

    def validate(self, data):
        if data['password'] != data.pop('confirm_password', None): # Remove confirm_password before saving
            raise serializers.ValidationError({"password": "Passwords do not match."})
        return data

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

#
# class CustomRegistrationSerializer(UserCreateSerializer):
#     class Meta:
#         model = User
#         fields = ['id', 'username', 'email', 'password','confirm_password','phone_number', 'role']
#         extra_kwargs = {'password': {'write_only': True}}
#
#     def create(self, validated_data):
#         user = User.objects.create_user(**validated_data)
#         return user

# # Login Serializer
# class LoginSerializer(serializers.Serializer):
#     username = serializers.CharField()
#     password = serializers.CharField(write_only=True)
#
#     def validate(self, data):
#         username = data.get('username')
#         password = data.get('password')
#
#         user = authenticate(username=username, password=password)
#
#         if user is None:
#             raise serializers.ValidationError("Invalid username or password")
#
#         # refresh = RefreshToken.for_user(user)
#         return data
#
#         # return {
#         #     'refresh': str(refresh),
#         #     'access': str(refresh.access_token),
#         #     'user': CustomRegistrationSerializer(user).data,
#         #     "message": "User registered successfully",
#         #
#         # }

class UserProfileSerializer(UserSerializer):
    class Meta(UserSerializer.Meta):
        model = User
        fields = ['id', 'username', 'email', 'phone_number', 'role']
        read_only_fields = ['id', 'username', 'role']  # Users cannot modify these fields


