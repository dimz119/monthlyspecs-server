# Item-Customer Many-to-Many Relationship

## 📋 Overview

This document explains the many-to-many relationship between Items and Customers, allowing customers to be associated with multiple items and items to be associated with multiple customers.

## 🔗 Relationship

**Many-to-Many: Item ↔ Customer**

- One item can be associated with multiple customers
- One customer can be associated with multiple items
- Managed through the `customers` field on the Item model
- Reverse relationship accessible via `customer.items.all()`

## 🏗️ Model Changes

### Item Model

```python
class Item(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    customers = models.ManyToManyField(Customer, related_name='items', blank=True)  # NEW!
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

### Customer Model

The reverse relationship `items` is automatically available:
```python
customer.items.all()  # Get all items for a customer
```

## 📡 API Endpoints

### Item Endpoints

```
GET    /api/items/                      - List all items
POST   /api/items/                      - Create a new item
GET    /api/items/{id}/                 - Get item details
PUT    /api/items/{id}/                 - Full update item
PATCH  /api/items/{id}/                 - Partial update item
DELETE /api/items/{id}/                 - Delete item
GET    /api/items/{id}/customers/       - Get all customers of an item
POST   /api/items/{id}/add_customer/    - Add a customer to an item
POST   /api/items/{id}/remove_customer/ - Remove a customer from an item
```

### Customer Endpoints (with Items)

```
GET    /api/customers/                  - List all customers (includes items)
POST   /api/customers/                  - Create a new customer
GET    /api/customers/{id}/             - Get customer details (includes items)
PATCH  /api/customers/{id}/             - Update customer (can update items)
POST   /api/customers/{id}/add_item/    - Add an item to a customer
POST   /api/customers/{id}/remove_item/ - Remove an item from a customer
```

## 📝 Usage Examples

### 1. Create an Item

```bash
curl -X POST http://localhost:8000/api/items/ \
  -H "Authorization: Token YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Premium Subscription",
    "description": "Annual premium membership"
  }'
```

**Response:**
```json
{
  "id": 1,
  "name": "Premium Subscription",
  "description": "Annual premium membership",
  "customer_count": 0,
  "customers_detail": [],
  "created_at": "2025-10-26T05:10:00Z",
  "updated_at": "2025-10-26T05:10:00Z"
}
```

### 2. Create an Item with Customers

```bash
curl -X POST http://localhost:8000/api/items/ \
  -H "Authorization: Token YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Basic Package",
    "description": "Starter package for new users",
    "customer_ids": [1, 2, 3]
  }'
```

### 3. Add a Customer to an Item

```bash
curl -X POST http://localhost:8000/api/items/1/add_customer/ \
  -H "Authorization: Token YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "customer_id": 5
  }'
```

**Response:**
```json
{
  "message": "Customer John Doe added to item"
}
```

### 4. Remove a Customer from an Item

```bash
curl -X POST http://localhost:8000/api/items/1/remove_customer/ \
  -H "Authorization: Token YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "customer_id": 5
  }'
```

**Response:**
```json
{
  "message": "Customer John Doe removed from item"
}
```

### 5. Get All Customers of an Item

```bash
curl -X GET http://localhost:8000/api/items/1/customers/ \
  -H "Authorization: Token YOUR_TOKEN"
```

**Response:**
```json
[
  {
    "id": 1,
    "username": "johndoe",
    "email": "john@example.com",
    "full_name": "John Doe",
    "phone": "+1-555-0199"
  },
  {
    "id": 2,
    "username": "janedoe",
    "email": "jane@example.com",
    "full_name": "Jane Doe",
    "phone": "+1-555-0200"
  }
]
```

### 6. Get Item Details (with Customers)

```bash
curl -X GET http://localhost:8000/api/items/1/ \
  -H "Authorization: Token YOUR_TOKEN"
```

**Response:**
```json
{
  "id": 1,
  "name": "Premium Subscription",
  "description": "Annual premium membership",
  "customer_count": 2,
  "customers_detail": [
    {
      "id": 1,
      "username": "johndoe",
      "email": "john@example.com",
      "full_name": "John Doe",
      "phone": "+1-555-0199"
    },
    {
      "id": 2,
      "username": "janedoe",
      "email": "jane@example.com",
      "full_name": "Jane Doe",
      "phone": "+1-555-0200"
    }
  ],
  "created_at": "2025-10-26T05:10:00Z",
  "updated_at": "2025-10-26T05:15:00Z"
}
```

### 7. Add an Item to a Customer

```bash
curl -X POST http://localhost:8000/api/customers/1/add_item/ \
  -H "Authorization: Token YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "item_id": 3
  }'
```

**Response:**
```json
{
  "message": "Item Basic Package added to customer"
}
```

### 8. Remove an Item from a Customer

```bash
curl -X POST http://localhost:8000/api/customers/1/remove_item/ \
  -H "Authorization: Token YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "item_id": 3
  }'
```

**Response:**
```json
{
  "message": "Item Basic Package removed from customer"
}
```

### 9. Get Customer Details (with Items)

```bash
curl -X GET http://localhost:8000/api/customers/1/ \
  -H "Authorization: Token YOUR_TOKEN"
```

**Response includes `items_detail`:**
```json
{
  "id": 1,
  "username": "johndoe",
  "email": "john@example.com",
  "full_name": "John Doe",
  "companies_detail": [...],
  "items_detail": [
    {
      "id": 1,
      "name": "Premium Subscription",
      "description": "Annual premium membership",
      "created_at": "2025-10-26T05:10:00Z",
      "updated_at": "2025-10-26T05:15:00Z"
    },
    {
      "id": 2,
      "name": "Pro Features",
      "description": "Advanced features package",
      "created_at": "2025-10-26T05:12:00Z",
      "updated_at": "2025-10-26T05:12:00Z"
    }
  ],
  "created_at": "2025-10-26T04:00:00Z",
  "updated_at": "2025-10-26T05:15:00Z"
}
```

### 10. Update Customer with Items

```bash
curl -X PATCH http://localhost:8000/api/customers/1/ \
  -H "Authorization: Token YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "item_ids": [1, 2, 3, 4]
  }'
```

### 11. Update Item with Customers

```bash
curl -X PATCH http://localhost:8000/api/items/1/ \
  -H "Authorization: Token YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Updated Premium Subscription",
    "customer_ids": [1, 2, 5, 7]
  }'
```

## 🎯 Swagger UI Examples

### Adding a Customer to an Item

1. Go to http://localhost:8000/api/docs/
2. Find `POST /api/items/{id}/add_customer/`
3. Enter the item ID (e.g., 1)
4. Click "Try it out"
5. Request body:

```json
{
  "customer_id": 2
}
```

6. Click "Execute"

### Creating an Item with Customers

1. Find `POST /api/items/`
2. Click "Try it out"
3. Request body:

```json
{
  "name": "Enterprise Package",
  "description": "Full-featured enterprise solution",
  "customer_ids": [1, 2, 3]
}
```

4. Click "Execute"

## 🔍 Querying in Django ORM

```python
from api.models import Customer, Item

# Get all items for a customer
customer = Customer.objects.get(id=1)
items = customer.items.all()

# Get all customers for an item
item = Item.objects.get(id=1)
customers = item.customers.all()

# Create item and add customers
item = Item.objects.create(name="New Item", description="Description")
customer1 = Customer.objects.get(id=1)
customer2 = Customer.objects.get(id=2)
item.customers.add(customer1, customer2)

# Filter items by customer
items_for_john = Item.objects.filter(customers__user__username='johndoe')

# Filter customers by item
customers_with_premium = Customer.objects.filter(items__name='Premium Subscription')

# Count customers per item
from django.db.models import Count
items_with_counts = Item.objects.annotate(customer_count=Count('customers'))

# Get items with more than 5 customers
popular_items = Item.objects.annotate(
    customer_count=Count('customers')
).filter(customer_count__gte=5)

# Get customers with specific items
customers_with_multiple_items = Customer.objects.annotate(
    item_count=Count('items')
).filter(item_count__gte=3)

# Add multiple items to a customer
customer = Customer.objects.get(id=1)
items = Item.objects.filter(id__in=[1, 2, 3])
customer.items.set(items)  # Replace all
# or
customer.items.add(*items)  # Add to existing

# Remove items from customer
customer.items.remove(item1, item2)

# Clear all items from customer
customer.items.clear()
```

## 📊 Complete Relationship Diagram

```
┌──────────────┐         ┌────────────────────┐         ┌──────────────┐
│    User      │         │     Customer       │         │   Company    │
├──────────────┤         ├────────────────────┤         ├──────────────┤
│ id (PK)      │◄────────│ user_id (FK, 1:1)  │◄───────►│ id (PK)      │
│ username     │         │ id (PK)            │  M:M    │ name         │
│ email        │         │ phone              │         │ ...          │
└──────────────┘         │ address            │         └──────────────┘
                         │ ...                │
                         └────────────────────┘
                                  ▲
                                  │
                                  │ M:M (NEW!)
                                  │
                                  ▼
                         ┌────────────────────┐
                         │       Item         │
                         ├────────────────────┤
                         │ id (PK)            │
                         │ name               │
                         │ description        │
                         │ created_at         │
                         │ updated_at         │
                         └────────────────────┘
```

## 💡 Use Cases

### 1. E-commerce / Shopping Cart
- Items = Products
- Customers purchase/favorite multiple products
- Products can be purchased by multiple customers

### 2. Subscription Management
- Items = Subscription plans/features
- Customers can subscribe to multiple plans
- Each plan can have multiple subscribers

### 3. Service Access Control
- Items = Services/Resources
- Customers can access multiple services
- Services can be accessed by multiple customers

### 4. License Management
- Items = Software licenses/modules
- Customers can own multiple licenses
- Licenses can be owned by multiple customers

### 5. Course Enrollment
- Items = Courses/Classes
- Customers (students) enroll in multiple courses
- Courses have multiple enrolled students

## 🚨 Important Notes

1. **Bidirectional Access**: You can manage the relationship from either side (Item or Customer)
2. **Auto-created Junction Table**: Django creates `api_item_customers` table automatically
3. **Bulk Operations**: Use `add()`, `remove()`, `set()`, `clear()` for efficient updates
4. **Query Performance**: Use `prefetch_related('customers')` or `prefetch_related('items')` to optimize queries
5. **API Flexibility**: Can update via PATCH with IDs or use dedicated add/remove endpoints

## 🎨 Serializer Response Structure

### ItemSerializer Response

```json
{
  "id": 1,
  "name": "Item name",
  "description": "Description",
  "customer_count": 3,                    // Count of associated customers
  "customers_detail": [                    // Full customer details (read-only)
    {
      "id": 1,
      "username": "johndoe",
      "email": "john@example.com",
      "full_name": "John Doe",
      "phone": "+1-555-0199"
    }
  ],
  "customer_ids": [1, 2, 3],              // For write operations
  "created_at": "2025-10-26T05:10:00Z",
  "updated_at": "2025-10-26T05:15:00Z"
}
```

### CustomerSerializer Response

```json
{
  "id": 1,
  "companies_detail": [...],
  "items_detail": [                        // Full item details (read-only)
    {
      "id": 1,
      "name": "Premium Subscription",
      "description": "Annual premium",
      "created_at": "2025-10-26T05:10:00Z",
      "updated_at": "2025-10-26T05:15:00Z"
    }
  ],
  "item_ids": [1, 2, 3],                  // For write operations
  ...
}
```

## 🎯 Next Steps

1. Add item categories/types
2. Add quantity or custom fields to the relationship (use explicit through model)
3. Add purchase history/timestamps
4. Add item availability/stock management
5. Add customer preferences for items
6. Add notifications when items are added/removed

---

**Happy Coding! 🚀**
