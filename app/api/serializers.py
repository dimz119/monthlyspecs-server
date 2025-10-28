from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Role, Item, Company, Customer, PurchaseHistory


class RoleSerializer(serializers.ModelSerializer):
    """Serializer for Role model"""
    customer_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Role
        fields = ['id', 'name', 'description', 'customer_count', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_customer_count(self, obj):
        """Get the number of customers with this role"""
        return obj.customers.count()


class CompanySerializer(serializers.ModelSerializer):
    """Serializer for Company model"""
    customer_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Company
        fields = [
            'id', 'name', 'description', 'address', 'phone', 
            'email', 'website', 'customer_count', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_customer_count(self, obj):
        """Get the number of customers associated with this company"""
        return obj.customers.count()


class ItemSummarySerializer(serializers.ModelSerializer):
    """Lightweight serializer for Item model (used in nested relationships)"""
    class Meta:
        model = Item
        fields = ['id', 'name', 'description', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class CustomerSummarySerializer(serializers.ModelSerializer):
    """Lightweight serializer for Customer model (used in nested relationships)"""
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)
    full_name = serializers.CharField(read_only=True)
    role_name = serializers.CharField(source='role.get_name_display', read_only=True)
    
    class Meta:
        model = Customer
        fields = ['id', 'username', 'email', 'full_name', 'phone', 'role_name']
        read_only_fields = ['id']


class CustomerSerializer(serializers.ModelSerializer):
    """Serializer for Customer model"""
    # Nested user information
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)
    first_name = serializers.CharField(source='user.first_name', read_only=True)
    last_name = serializers.CharField(source='user.last_name', read_only=True)
    full_name = serializers.CharField(read_only=True)
    
    # Role information
    role_detail = RoleSerializer(source='role', read_only=True)
    role_id = serializers.PrimaryKeyRelatedField(
        queryset=Role.objects.all(),
        source='role',
        write_only=True,
        required=False
    )
    
    # Companies as nested objects (read) or IDs (write)
    companies_detail = CompanySerializer(source='companies', many=True, read_only=True)
    company_ids = serializers.PrimaryKeyRelatedField(
        many=True, 
        queryset=Company.objects.all(),
        source='companies',
        write_only=True,
        required=False
    )
    
    # Items as nested objects (read) or IDs (write)
    items_detail = ItemSummarySerializer(source='items', many=True, read_only=True)
    item_ids = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Item.objects.all(),
        source='items',
        write_only=True,
        required=False
    )
    
    class Meta:
        model = Customer
        fields = [
            'id', 'user', 'username', 'email', 'first_name', 'last_name', 
            'full_name', 'role_detail', 'role_id', 'phone', 'address', 'date_of_birth', 
            'profile_picture', 'bio', 'companies_detail', 'company_ids',
            'items_detail', 'item_ids', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'user']


class CustomerCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating a Customer with a new User"""
    # User fields for creation
    username = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})
    email = serializers.EmailField(write_only=True)
    first_name = serializers.CharField(write_only=True, required=False, allow_blank=True)
    last_name = serializers.CharField(write_only=True, required=False, allow_blank=True)
    
    # Role ID (optional, defaults to 'customer' if not provided)
    role_id = serializers.PrimaryKeyRelatedField(
        queryset=Role.objects.all(),
        source='role',
        required=False
    )
    
    # Company IDs for many-to-many relationship
    company_ids = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Company.objects.all(),
        source='companies',
        required=False
    )
    
    class Meta:
        model = Customer
        fields = [
            'username', 'password', 'email', 'first_name', 'last_name',
            'phone', 'address', 'date_of_birth', 'profile_picture', 
            'bio', 'role_id', 'company_ids'
        ]
    
    def create(self, validated_data):
        # Extract user data
        username = validated_data.pop('username')
        password = validated_data.pop('password')
        email = validated_data.pop('email')
        first_name = validated_data.pop('first_name', '')
        last_name = validated_data.pop('last_name', '')
        
        # Extract companies (if provided)
        companies = validated_data.pop('companies', [])
        
        # Get or set role (default to 'customer' if not provided)
        role = validated_data.pop('role', None)
        if role is None:
            role, _ = Role.objects.get_or_create(
                name=Role.CUSTOMER,
                defaults={'description': 'Standard customer role'}
            )
        
        # Create User
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )
        
        # Create Customer with role
        customer = Customer.objects.create(user=user, role=role, **validated_data)
        
        # Add companies
        if companies:
            customer.companies.set(companies)
        
        return customer


class ItemSerializer(serializers.ModelSerializer):
    """Serializer for Item model"""
    customer_count = serializers.SerializerMethodField()
    customers_detail = CustomerSummarySerializer(source='customers', many=True, read_only=True)
    customer_ids = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Customer.objects.all(),
        source='customers',
        write_only=True,
        required=False
    )
    
    class Meta:
        model = Item
        fields = [
            'id', 'name', 'description', 'unit_price', 'customer_count', 
            'customers_detail', 'customer_ids', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_customer_count(self, obj):
        """Get the number of customers associated with this item"""
        return obj.customers.count()


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


class PurchaseHistorySerializer(serializers.ModelSerializer):
    """Serializer for PurchaseHistory model"""
    customer_username = serializers.CharField(source='customer.user.username', read_only=True)
    customer_email = serializers.CharField(source='customer.user.email', read_only=True)
    item_name = serializers.CharField(source='item.name', read_only=True)
    item_description = serializers.CharField(source='item.description', read_only=True)
    unit_price = serializers.DecimalField(source='item.unit_price', max_digits=10, decimal_places=2, read_only=True)
    total_price = serializers.SerializerMethodField()
    
    class Meta:
        model = PurchaseHistory
        fields = [
            'id', 'customer', 'customer_username', 'customer_email',
            'item', 'item_name', 'item_description',
            'quantity', 'unit_price', 'total_price',
            'purchase_date', 'notes',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'unit_price', 'total_price', 'purchase_date', 'created_at', 'updated_at']
    
    def get_total_price(self, obj):
        """Calculate total price"""
        return obj.total_price
    
    def validate_quantity(self, value):
        """Validate that quantity is positive"""
        if value <= 0:
            raise serializers.ValidationError("Quantity must be greater than 0")
        return value


class PurchaseHistorySummarySerializer(serializers.ModelSerializer):
    """Lightweight serializer for PurchaseHistory (for nested use)"""
    item_name = serializers.CharField(source='item.name', read_only=True)
    total_price = serializers.SerializerMethodField()
    
    class Meta:
        model = PurchaseHistory
        fields = ['id', 'item_name', 'quantity', 'total_price', 'purchase_date']
        read_only_fields = ['id', 'total_price', 'purchase_date']
    
    def get_total_price(self, obj):
        """Calculate total price"""
        return obj.total_price
