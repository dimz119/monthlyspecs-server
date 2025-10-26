from django.contrib import admin
from .models import Role, Company, Customer, Item


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ['name', 'get_customer_count', 'created_at']
    search_fields = ['name', 'description']
    list_filter = ['name']
    ordering = ['name']
    
    def get_customer_count(self, obj):
        return obj.customers.count()
    get_customer_count.short_description = 'Customer Count'


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'phone', 'created_at']
    search_fields = ['name', 'email', 'phone']
    list_filter = ['created_at']
    ordering = ['name']


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['user', 'role', 'get_email', 'phone', 'created_at']
    search_fields = ['user__username', 'user__email', 'user__first_name', 'user__last_name', 'phone']
    list_filter = ['created_at', 'role', 'companies']
    filter_horizontal = ['companies']
    raw_id_fields = ['user', 'role']
    
    def get_email(self, obj):
        return obj.user.email
    get_email.short_description = 'Email'
    get_email.admin_order_field = 'user__email'


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'get_customer_count', 'created_at', 'updated_at']
    search_fields = ['name', 'description']
    list_filter = ['created_at']
    filter_horizontal = ['customers']
    ordering = ['-created_at']
    
    def get_customer_count(self, obj):
        return obj.customers.count()
    get_customer_count.short_description = 'Customer Count'
