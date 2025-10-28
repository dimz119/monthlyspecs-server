from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Role(models.Model):
    """Role model for defining user roles"""
    OWNER = 'owner'
    MANAGER = 'manager'
    CUSTOMER = 'customer'
    
    ROLE_CHOICES = [
        (OWNER, 'Owner'),
        (MANAGER, 'Manager'),
        (CUSTOMER, 'Customer'),
    ]
    
    name = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        unique=True,
        help_text="Role name: owner, manager, or customer"
    )
    description = models.TextField(blank=True, help_text="Description of the role")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return self.get_name_display()


class Company(models.Model):
    """Company model"""
    name = models.CharField(max_length=200, unique=True)
    description = models.TextField(blank=True)
    address = models.TextField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    website = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['name']
        verbose_name_plural = 'Companies'
    
    def __str__(self):
        return self.name


class Customer(models.Model):
    """Customer model extending Django User with additional fields"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='customer')
    role = models.ForeignKey(
        Role,
        on_delete=models.PROTECT,
        related_name='customers',
        help_text="User role: owner, manager, or customer"
    )
    companies = models.ManyToManyField(Company, related_name='customers', blank=True)
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    profile_picture = models.URLField(blank=True, help_text="URL to profile picture")
    bio = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.user.get_full_name() or 'No name'} ({self.role})"
    
    @property
    def full_name(self):
        """Get full name from associated User"""
        return self.user.get_full_name() or self.user.username
    
    @property
    def email(self):
        """Get email from associated User"""
        return self.user.email


class Item(models.Model):
    """Sample model for demonstration"""
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    unit_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        help_text="Price per unit"
    )
    customers = models.ManyToManyField(Customer, related_name='items', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.name


class PurchaseHistory(models.Model):
    """Purchase history model to track customer purchases"""
    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        related_name='purchase_history',
        help_text="Customer who made the purchase"
    )
    item = models.ForeignKey(
        Item,
        on_delete=models.PROTECT,
        related_name='purchase_history',
        help_text="Item that was purchased"
    )
    quantity = models.PositiveIntegerField(default=1, help_text="Quantity purchased")
    purchase_date = models.DateTimeField(auto_now_add=True, help_text="Date and time of purchase")
    notes = models.TextField(blank=True, help_text="Additional notes about the purchase")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-purchase_date']
        verbose_name_plural = 'Purchase Histories'
        indexes = [
            models.Index(fields=['-purchase_date']),
            models.Index(fields=['customer', '-purchase_date']),
        ]
    
    def __str__(self):
        return f"{self.customer.user.username} - {self.item.name} ({self.quantity}) on {self.purchase_date.strftime('%Y-%m-%d')}"
    
    @property
    def unit_price(self):
        """Get unit price from the item"""
        return self.item.unit_price
    
    @property
    def total_price(self):
        """Calculate total price based on quantity and item's unit price"""
        return self.quantity * self.item.unit_price

