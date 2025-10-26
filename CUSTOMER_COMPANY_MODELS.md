# Customer and Company Models - Documentation

## 📋 Overview

This document explains the Customer and Company models and their many-to-many relationship.

## 🏗️ Model Structure

### Company Model

Represents a business organization.

**Fields:**
- `id` (AutoField) - Primary key
- `name` (CharField, max 200, unique) - Company name
- `description` (TextField, optional) - Company description
- `address` (TextField, optional) - Physical address
- `phone` (CharField, max 20, optional) - Contact phone
- `email` (EmailField, optional) - Contact email
- `website` (URLField, optional) - Company website
- `created_at` (DateTimeField) - Auto-set on creation
- `updated_at` (DateTimeField) - Auto-updated on save

### Customer Model

Extends Django's User model with additional fields and company relationships.

**Fields:**
- `id` (AutoField) - Primary key
- `user` (OneToOneField to User) - Link to Django User
- `companies` (ManyToManyField to Company) - Associated companies
- `phone` (CharField, max 20, optional) - Phone number
- `address` (TextField, optional) - Physical address
- `date_of_birth` (DateField, optional) - Birth date
- `profile_picture` (URLField, optional) - Profile picture URL
- `bio` (TextField, optional) - Customer biography
- `created_at` (DateTimeField) - Auto-set on creation
- `updated_at` (DateTimeField) - Auto-updated on save

**Properties:**
- `full_name` - Returns user's full name or username
- `email` - Returns user's email address

## 🔗 Relationships

### Many-to-Many: Customer ↔ Company

- One customer can belong to multiple companies
- One company can have multiple customers
- Managed through the `companies` field on Customer model
- Reverse relationship accessible via `company.customers.all()`

## 🚀 API Endpoints

### Company Endpoints

```
GET    /api/companies/              - List all companies
POST   /api/companies/              - Create a new company
GET    /api/companies/{id}/         - Get company details
PUT    /api/companies/{id}/         - Full update company
PATCH  /api/companies/{id}/         - Partial update company
DELETE /api/companies/{id}/         - Delete company
GET    /api/companies/{id}/customers/ - Get all customers of a company
```

### Customer Endpoints

```
GET    /api/customers/                     - List all customers
POST   /api/customers/                     - Create a new customer (with User)
GET    /api/customers/{id}/                - Get customer details
PUT    /api/customers/{id}/                - Full update customer
PATCH  /api/customers/{id}/                - Partial update customer
DELETE /api/customers/{id}/                - Delete customer
POST   /api/customers/{id}/add_company/    - Add a company to customer
POST   /api/customers/{id}/remove_company/ - Remove a company from customer
```

## 📝 Usage Examples

### 1. Create a Company

```bash
curl -X POST http://localhost:8000/api/companies/ \
  -H "Authorization: Token YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Acme Corporation",
    "description": "Leading provider of innovative solutions",
    "email": "contact@acme.com",
    "phone": "+1-555-0123",
    "website": "https://acme.com",
    "address": "123 Main St, City, State 12345"
  }'
```

**Response:**
```json
{
  "id": 1,
  "name": "Acme Corporation",
  "description": "Leading provider of innovative solutions",
  "address": "123 Main St, City, State 12345",
  "phone": "+1-555-0123",
  "email": "contact@acme.com",
  "website": "https://acme.com",
  "customer_count": 0,
  "created_at": "2025-10-26T05:00:00Z",
  "updated_at": "2025-10-26T05:00:00Z"
}
```

### 2. Create a Customer (with new User)

```bash
curl -X POST http://localhost:8000/api/customers/ \
  -H "Authorization: Token YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "johndoe",
    "password": "SecurePass123!",
    "email": "john@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "phone": "+1-555-0199",
    "address": "456 Oak Ave, City, State 12345",
    "date_of_birth": "1990-01-15",
    "bio": "Software developer and tech enthusiast",
    "company_ids": [1]
  }'
```

**Response:**
```json
{
  "id": 1,
  "user": 2,
  "username": "johndoe",
  "email": "john@example.com",
  "first_name": "John",
  "last_name": "Doe",
  "full_name": "John Doe",
  "phone": "+1-555-0199",
  "address": "456 Oak Ave, City, State 12345",
  "date_of_birth": "1990-01-15",
  "profile_picture": "",
  "bio": "Software developer and tech enthusiast",
  "companies_detail": [
    {
      "id": 1,
      "name": "Acme Corporation",
      ...
    }
  ],
  "created_at": "2025-10-26T05:00:00Z",
  "updated_at": "2025-10-26T05:00:00Z"
}
```

### 3. List All Customers

```bash
curl -X GET http://localhost:8000/api/customers/ \
  -H "Authorization: Token YOUR_TOKEN"
```

### 4. Get Customer Details

```bash
curl -X GET http://localhost:8000/api/customers/1/ \
  -H "Authorization: Token YOUR_TOKEN"
```

### 5. Add Company to Customer

```bash
curl -X POST http://localhost:8000/api/customers/1/add_company/ \
  -H "Authorization: Token YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "company_id": 2
  }'
```

**Response:**
```json
{
  "message": "Company Tech Innovations added to customer"
}
```

### 6. Remove Company from Customer

```bash
curl -X POST http://localhost:8000/api/customers/1/remove_company/ \
  -H "Authorization: Token YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "company_id": 2
  }'
```

**Response:**
```json
{
  "message": "Company Tech Innovations removed from customer"
}
```

### 7. Get All Customers of a Company

```bash
curl -X GET http://localhost:8000/api/companies/1/customers/ \
  -H "Authorization: Token YOUR_TOKEN"
```

### 8. Update Customer Profile

```bash
curl -X PATCH http://localhost:8000/api/customers/1/ \
  -H "Authorization: Token YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "phone": "+1-555-9999",
    "bio": "Updated bio information",
    "company_ids": [1, 2, 3]
  }'
```

## 🎯 Swagger UI Examples

### Creating a Customer

1. Go to http://localhost:8000/api/docs/
2. Click "Authorize" and enter your token
3. Find `POST /api/customers/`
4. Click "Try it out"
5. Fill in the request body:

```json
{
  "username": "janedoe",
  "password": "SecurePass456!",
  "email": "jane@example.com",
  "first_name": "Jane",
  "last_name": "Doe",
  "phone": "+1-555-0200",
  "company_ids": [1]
}
```

6. Click "Execute"

### Adding a Company to Customer

1. Find `POST /api/customers/{id}/add_company/`
2. Enter customer ID (e.g., 1)
3. Click "Try it out"
4. Request body:

```json
{
  "company_id": 2
}
```

5. Click "Execute"

## 🔍 Querying in Python

### Using Django ORM

```python
from api.models import Customer, Company

# Get all customers of a company
company = Company.objects.get(id=1)
customers = company.customers.all()

# Get all companies of a customer
customer = Customer.objects.get(id=1)
companies = customer.companies.all()

# Create customer with companies
user = User.objects.create_user(username='newuser', password='pass123')
customer = Customer.objects.create(user=user, phone='+1-555-0300')
customer.companies.add(company1, company2)

# Filter customers by company
customers_in_acme = Customer.objects.filter(companies__name='Acme Corporation')

# Filter companies by customer count
popular_companies = Company.objects.annotate(
    customer_count=Count('customers')
).filter(customer_count__gte=10)
```

## 🏛️ Admin Panel

Both models are registered in the Django admin panel:

- Access at: http://localhost:8000/admin/
- **Companies**: Searchable by name, email, phone
- **Customers**: Searchable by username, email, name, phone
  - Filter by company and creation date
  - Horizontal filter for managing company relationships

## 🎨 Model Design Decisions

### Why OneToOne for User?

- Each customer profile is tied to exactly one Django User
- Keeps authentication separate from business logic
- Allows using Django's built-in auth system
- Customer is deleted if User is deleted (CASCADE)

### Why ManyToMany for Companies?

- Real-world scenario: customers can work with multiple companies
- Companies can have multiple customers
- Flexible relationship management
- No limit on number of associations

### Additional Fields

- `created_at`/`updated_at`: Track record lifecycle
- `profile_picture` as URL: Assumes external storage (S3, CDN)
- `bio`: For customer self-description
- Properties (`full_name`, `email`): Convenient access to User data

## 🔐 Permissions

All endpoints require authentication (`IsAuthenticated`).

To customize permissions:

```python
# In views.py
class CustomerViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
```

## 📊 Database Schema

```
┌──────────────┐         ┌────────────────────┐         ┌──────────────┐
│    User      │         │     Customer       │         │   Company    │
├──────────────┤         ├────────────────────┤         ├──────────────┤
│ id (PK)      │◄────────│ user_id (FK, 1:1)  │         │ id (PK)      │
│ username     │         │ id (PK)            │         │ name         │
│ email        │         │ phone              │         │ description  │
│ password     │         │ address            │◄────────►│ email        │
│ first_name   │         │ date_of_birth      │  M:M    │ phone        │
│ last_name    │         │ profile_picture    │         │ website      │
└──────────────┘         │ bio                │         │ address      │
                         │ created_at         │         │ created_at   │
                         │ updated_at         │         │ updated_at   │
                         └────────────────────┘         └──────────────┘
                                  ▲                            ▲
                                  │                            │
                                  └────────────────────────────┘
                                    customer_companies (M:M table)
```

## 🚨 Important Notes

1. **Creating Customers**: Use `POST /api/customers/` to create both User and Customer in one request
2. **Deleting Users**: Deleting a User will also delete the associated Customer (CASCADE)
3. **Unique Usernames**: Django User requires unique usernames
4. **Company Names**: Company names must be unique
5. **Password Security**: Passwords are hashed using Django's auth system

## 🎯 Next Steps

1. Add custom permissions (e.g., customers can only edit their own profile)
2. Add filtering/search capabilities to list endpoints
3. Add profile picture upload functionality
4. Add email verification for new customers
5. Add company membership approval workflow
6. Add role-based access within companies

---

**Happy Coding! 🚀**
