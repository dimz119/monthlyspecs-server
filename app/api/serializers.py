from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Item


class ItemSerializer(serializers.ModelSerializer):
    """Serializer for Item model"""
    class Meta:
        model = Item
        fields = ['id', 'name', 'description', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model"""
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']
        read_only_fields = ['id']


class LoginSerializer(serializers.Serializer):
    """Serializer for login request"""
    username = serializers.CharField(required=True, help_text="Username for authentication")
    password = serializers.CharField(
        required=True, 
        write_only=True, 
        style={'input_type': 'password'},
        help_text="Password for authentication"
    )


class AuthTokenSerializer(serializers.Serializer):
    """Serializer for authentication token response"""
    token = serializers.CharField(read_only=True, help_text="Authentication token - use as: Authorization: Token <token>")
    user_id = serializers.IntegerField(read_only=True)
    username = serializers.CharField(read_only=True)
    email = serializers.EmailField(read_only=True)
    auth_header = serializers.CharField(
        read_only=True, 
        help_text="Complete authorization header value to copy-paste"
    )


class LogoutResponseSerializer(serializers.Serializer):
    """Serializer for logout response"""
    message = serializers.CharField(read_only=True)
