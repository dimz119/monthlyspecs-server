from rest_framework import viewsets, permissions, status
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from drf_spectacular.utils import extend_schema, OpenApiExample
from .models import Role, Item, Company, Customer, PurchaseHistory
from .serializers import (
    RoleSerializer,
    ItemSerializer, 
    UserSerializer, 
    LoginSerializer, 
    AuthTokenSerializer,
    LogoutResponseSerializer,
    CompanySerializer,
    CustomerSerializer,
    CustomerCreateSerializer,
    PurchaseHistorySerializer
)


class RoleViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint for viewing roles.
    Supports GET operations only (roles are predefined).
    """
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    @action(detail=True, methods=['get'])
    def customers(self, request, pk=None):
        """Get all customers with this role"""
        role = self.get_object()
        customers = role.customers.all()
        serializer = CustomerSerializer(customers, many=True)
        return Response(serializer.data)


class CompanyViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing companies.
    Supports GET, POST, PUT, PATCH, DELETE operations.
    """
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [permissions.IsAuthenticated]
    
    @action(detail=True, methods=['get'])
    def customers(self, request, pk=None):
        """Get all customers associated with this company"""
        company = self.get_object()
        customers = company.customers.all()
        serializer = CustomerSerializer(customers, many=True)
        return Response(serializer.data)


class CustomerViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing customers.
    Supports GET, POST, PUT, PATCH, DELETE operations.
    """
    queryset = Customer.objects.select_related('user').prefetch_related('companies').all()
    permission_classes = [permissions.IsAuthenticated]
    
    def get_serializer_class(self):
        """Use different serializer for creation"""
        if self.action == 'create':
            return CustomerCreateSerializer
        return CustomerSerializer
    
    @action(detail=True, methods=['post'])
    def add_company(self, request, pk=None):
        """Add a company to this customer"""
        customer = self.get_object()
        company_id = request.data.get('company_id')
        
        try:
            company = Company.objects.get(id=company_id)
            customer.companies.add(company)
            return Response({'message': f'Company {company.name} added to customer'})
        except Company.DoesNotExist:
            return Response(
                {'error': 'Company not found'},
                status=status.HTTP_404_NOT_FOUND
            )
    
    @action(detail=True, methods=['post'])
    def remove_company(self, request, pk=None):
        """Remove a company from this customer"""
        customer = self.get_object()
        company_id = request.data.get('company_id')
        
        try:
            company = Company.objects.get(id=company_id)
            customer.companies.remove(company)
            return Response({'message': f'Company {company.name} removed from customer'})
        except Company.DoesNotExist:
            return Response(
                {'error': 'Company not found'},
                status=status.HTTP_404_NOT_FOUND
            )
    
    @action(detail=True, methods=['post'])
    def add_item(self, request, pk=None):
        """Add an item to this customer"""
        customer = self.get_object()
        item_id = request.data.get('item_id')
        
        try:
            item = Item.objects.get(id=item_id)
            customer.items.add(item)
            return Response({'message': f'Item {item.name} added to customer'})
        except Item.DoesNotExist:
            return Response(
                {'error': 'Item not found'},
                status=status.HTTP_404_NOT_FOUND
            )
    
    @action(detail=True, methods=['post'])
    def remove_item(self, request, pk=None):
        """Remove an item from this customer"""
        customer = self.get_object()
        item_id = request.data.get('item_id')
        
        try:
            item = Item.objects.get(id=item_id)
            customer.items.remove(item)
            return Response({'message': f'Item {item.name} removed from customer'})
        except Item.DoesNotExist:
            return Response(
                {'error': 'Item not found'},
                status=status.HTTP_404_NOT_FOUND
            )


class ItemViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing items.
    Supports GET, POST, PUT, PATCH, DELETE operations.
    """
    queryset = Item.objects.prefetch_related('customers').all()
    serializer_class = ItemSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    @action(detail=True, methods=['get'])
    def customers(self, request, pk=None):
        """Get all customers associated with this item"""
        item = self.get_object()
        customers = item.customers.all()
        from .serializers import CustomerSummarySerializer
        serializer = CustomerSummarySerializer(customers, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def add_customer(self, request, pk=None):
        """Add a customer to this item"""
        item = self.get_object()
        customer_id = request.data.get('customer_id')
        
        try:
            customer = Customer.objects.get(id=customer_id)
            item.customers.add(customer)
            return Response({'message': f'Customer {customer.full_name} added to item'})
        except Customer.DoesNotExist:
            return Response(
                {'error': 'Customer not found'},
                status=status.HTTP_404_NOT_FOUND
            )
    
    @action(detail=True, methods=['post'])
    def remove_customer(self, request, pk=None):
        """Remove a customer from this item"""
        item = self.get_object()
        customer_id = request.data.get('customer_id')
        
        try:
            customer = Customer.objects.get(id=customer_id)
            item.customers.remove(customer)
            return Response({'message': f'Customer {customer.full_name} removed from item'})
        except Customer.DoesNotExist:
            return Response(
                {'error': 'Customer not found'},
                status=status.HTTP_404_NOT_FOUND
            )


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


class PurchaseHistoryViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing purchase history.
    Supports filtering by customer.
    
    Query Parameters:
    - customer: Filter by customer ID
    - customer__user__username: Filter by username
    """
    queryset = PurchaseHistory.objects.select_related('customer', 'customer__user', 'item').all()
    serializer_class = PurchaseHistorySerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ['customer', 'item', 'customer__user__username']
    ordering_fields = ['purchase_date', 'total_price', 'quantity']
    ordering = ['-purchase_date']
    
    def get_queryset(self):
        """
        Optionally filter purchases by customer.
        Non-staff users can only see their own purchase history.
        """
        queryset = super().get_queryset()
        
        # If user is not staff, only show their own purchase history
        if not self.request.user.is_staff:
            try:
                customer = Customer.objects.get(user=self.request.user)
                queryset = queryset.filter(customer=customer)
            except Customer.DoesNotExist:
                queryset = queryset.none()
        
        return queryset
    
    @action(detail=False, methods=['get'])
    def my_purchases(self, request):
        """Get purchase history for the authenticated user"""
        try:
            customer = Customer.objects.get(user=request.user)
            purchases = self.get_queryset().filter(customer=customer)
            
            page = self.paginate_queryset(purchases)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)
            
            serializer = self.get_serializer(purchases, many=True)
            return Response(serializer.data)
        except Customer.DoesNotExist:
            return Response(
                {'error': 'Customer profile not found'},
                status=status.HTTP_404_NOT_FOUND
            )
    
    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """Get purchase statistics for the authenticated user"""
        try:
            customer = Customer.objects.get(user=request.user)
            purchases = self.get_queryset().filter(customer=customer)
            
            total_purchases = purchases.count()
            total_spent = sum(p.total_price for p in purchases)
            
            return Response({
                'total_purchases': total_purchases,
                'total_spent': str(total_spent),
                'average_purchase': str(total_spent / total_purchases) if total_purchases > 0 else '0.00'
            })
        except Customer.DoesNotExist:
            return Response(
                {'error': 'Customer profile not found'},
                status=status.HTTP_404_NOT_FOUND
            )
