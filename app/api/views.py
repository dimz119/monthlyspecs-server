from rest_framework import viewsets, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from drf_spectacular.utils import extend_schema, OpenApiExample
from .models import Item
from .serializers import (
    ItemSerializer, 
    UserSerializer, 
    LoginSerializer, 
    AuthTokenSerializer,
    LogoutResponseSerializer
)


class ItemViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing items.
    Supports GET, POST, PUT, PATCH, DELETE operations.
    """
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    permission_classes = [permissions.IsAuthenticated]


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint for viewing users.
    Read-only access to user information.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
@extend_schema(
    summary="User Login",
    description="Authenticate user and receive an authentication token. Use this token in the Authorization header as: `Token <your-token>`",
    request=LoginSerializer,
    responses={
        200: AuthTokenSerializer,
        400: {'description': 'Missing username or password'},
        401: {'description': 'Invalid credentials'},
    },
    examples=[
        OpenApiExample(
            'Login Example',
            value={
                'username': 'admin',
                'password': 'your-password'
            },
            request_only=True
        ),
        OpenApiExample(
            'Success Response',
            value={
                'token': 'd001965bba4175157d705255a5c8f2291a59286a',
                'user_id': 1,
                'username': 'admin',
                'email': 'admin@example.com',
                'auth_header': 'Token d001965bba4175157d705255a5c8f2291a59286a'
            },
            response_only=True,
            status_codes=['200']
        )
    ]
)
def login_view(request):
    """
    API endpoint for user login.
    Returns authentication token on successful login.
    
    **Important:** When making authenticated requests, include the token in the header as:
    ```
    Authorization: Token <your-token>
    ```
    
    Example:
    ```
    Authorization: Token d001965bba4175157d705255a5c8f2291a59286a
    ```
    """
    serializer = LoginSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    
    username = serializer.validated_data['username']
    password = serializer.validated_data['password']
    
    user = authenticate(username=username, password=password)
    
    if not user:
        return Response(
            {'error': 'Invalid credentials'},
            status=status.HTTP_401_UNAUTHORIZED
        )
    
    token, created = Token.objects.get_or_create(user=user)
    
    return Response({
        'token': token.key,
        'user_id': user.id,
        'username': user.username,
        'email': user.email,
        'auth_header': f'Token {token.key}'
    })


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
@extend_schema(
    summary="User Logout",
    description="Logout user by deleting their authentication token",
    request=None,
    responses={
        200: LogoutResponseSerializer,
        500: {'description': 'Internal server error'},
    }
)
def logout_view(request):
    """
    API endpoint for user logout.
    Deletes the authentication token.
    """
    try:
        request.user.auth_token.delete()
        return Response({'message': 'Successfully logged out'})
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
