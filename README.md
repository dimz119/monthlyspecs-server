# MonthlySpecs Server

A Django REST Framework API with web-based authentication, token authentication, and comprehensive customer/company management.

## Features

### 🔐 Dual Authentication System

- **Web Authentication** (django-allauth)
  - User signup and login pages
  - Session-based authentication for browser access
  - Dashboard for logged-in users
  - Automatic customer profile creation on signup
  
- **API Token Authentication**
  - Token-based authentication for API clients
  - Swagger UI integration with persistent token storage
  - Secure API access for external applications

### 📊 Data Models

- **Customer** - User profiles with phone, address, bio, and profile picture
- **Company** - Business entities with contact information
- **Item** - Products/items with descriptions
- **Many-to-Many Relationships**:
  - Customer ↔ Company
  - Customer ↔ Item

### 📚 Interactive Documentation

- **Swagger UI** (`/api/docs/`) - Interactive API testing
- **ReDoc** (`/api/redoc/`) - Alternative API documentation
- **OpenAPI 3.0 Schema** - Standard API specification

## Quick Start

### 1. Installation

```bash
# Clone the repository
cd monthlyspecs-server

# Install dependencies using uv
uv sync

# Activate virtual environment
source .venv/bin/activate

# Run migrations
cd app
python manage.py migrate

# Create a superuser (optional)
python manage.py createsuperuser

# Start the development server
python manage.py runserver
```

### 2. Access the Application

**Web Interface:**
- Home: http://localhost:8000/
- Sign Up: http://localhost:8000/accounts/signup/
- Login: http://localhost:8000/accounts/login/
- Dashboard: http://localhost:8000/dashboard/ (requires login)
- Admin: http://localhost:8000/admin/

**API Documentation:**
- Swagger UI: http://localhost:8000/api/docs/
- ReDoc: http://localhost:8000/api/redoc/
- OpenAPI Schema: http://localhost:8000/api/schema/

### 3. Create Your First Account

1. Visit http://localhost:8000/accounts/signup/
2. Fill in username, email, and password
3. Submit the form
4. You'll be redirected to the dashboard
5. A Customer profile is automatically created for you!

### 4. Get Your API Token

**Option A: Using curl**
```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "your_username", "password": "your_password"}'
```

**Option B: Using Swagger UI**
1. Go to http://localhost:8000/api/docs/
2. Find `/api/auth/login/` endpoint
3. Click "Try it out"
4. Enter your credentials
5. Click "Execute"
6. Copy the token from the response

### 5. Use the API

```bash
# List all companies (requires authentication)
curl http://localhost:8000/api/companies/ \
  -H "Authorization: Token YOUR_TOKEN_HERE"

# List all customers
curl http://localhost:8000/api/customers/ \
  -H "Authorization: Token YOUR_TOKEN_HERE"

# Create a new company
curl -X POST http://localhost:8000/api/companies/ \
  -H "Authorization: Token YOUR_TOKEN_HERE" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Acme Corp",
    "email": "contact@acme.com",
    "phone": "555-1234",
    "address": "123 Main St"
  }'
```

## Project Structure

```
monthlyspecs-server/
├── app/
│   ├── api/                      # Main API application
│   │   ├── models.py             # Data models (Customer, Company, Item)
│   │   ├── serializers.py        # DRF serializers
│   │   ├── views.py              # API viewsets
│   │   ├── web_views.py          # Web page views (home, dashboard)
│   │   ├── urls.py               # API URL routing
│   │   ├── web_urls.py           # Web page URL routing
│   │   ├── admin.py              # Admin panel configuration
│   │   └── signals.py            # Django signals (auto-create Customer)
│   ├── app/
│   │   ├── settings.py           # Django settings
│   │   ├── urls.py               # Main URL configuration
│   │   └── wsgi.py               # WSGI configuration
│   ├── templates/                # HTML templates
│   │   ├── base.html             # Base template
│   │   ├── home.html             # Landing page
│   │   ├── dashboard.html        # User dashboard
│   │   └── account/
│   │       ├── login.html        # Login page
│   │       └── signup.html       # Signup page
│   ├── manage.py                 # Django management script
│   └── db.sqlite3                # SQLite database
├── pyproject.toml                # Project dependencies
├── uv.lock                       # Lock file for dependencies
└── README.md                     # This file
```

## API Endpoints

### Authentication
- `POST /api/auth/login/` - Get authentication token
- `POST /api/auth/logout/` - Logout (invalidate token)

### Companies
- `GET /api/companies/` - List all companies
- `POST /api/companies/` - Create a new company
- `GET /api/companies/{id}/` - Get company details
- `PUT /api/companies/{id}/` - Update company
- `DELETE /api/companies/{id}/` - Delete company
- `GET /api/companies/{id}/customers/` - List company's customers
- `POST /api/companies/{id}/add_customer/` - Add customer to company
- `POST /api/companies/{id}/remove_customer/` - Remove customer from company

### Customers
- `GET /api/customers/` - List all customers
- `POST /api/customers/` - Create a new customer
- `GET /api/customers/{id}/` - Get customer details
- `PUT /api/customers/{id}/` - Update customer
- `DELETE /api/customers/{id}/` - Delete customer
- `POST /api/customers/{id}/add_company/` - Add company to customer
- `POST /api/customers/{id}/remove_company/` - Remove company from customer
- `POST /api/customers/{id}/add_item/` - Add item to customer
- `POST /api/customers/{id}/remove_item/` - Remove item from customer

### Items
- `GET /api/items/` - List all items
- `POST /api/items/` - Create a new item
- `GET /api/items/{id}/` - Get item details
- `PUT /api/items/{id}/` - Update item
- `DELETE /api/items/{id}/` - Delete item
- `GET /api/items/{id}/customers/` - List item's customers
- `POST /api/items/{id}/add_customer/` - Add customer to item
- `POST /api/items/{id}/remove_customer/` - Remove customer from item

### Users
- `GET /api/users/` - List all users
- `GET /api/users/{id}/` - Get user details

## Technologies

- **Django 5.2.7** - Web framework
- **Django REST Framework 3.16.1** - API framework
- **django-allauth 65.3.0** - Web authentication
- **drf-spectacular 0.28.0** - OpenAPI schema generation
- **Python 3.13** - Programming language
- **SQLite** - Database
- **uv** - Fast Python package installer

## Documentation Files

- [WEB_AUTH_GUIDE.md](app/WEB_AUTH_GUIDE.md) - Web authentication setup and usage
- [API_GUIDE.md](app/API_GUIDE.md) - Complete API documentation
- [TOKEN_AUTH_GUIDE.md](app/TOKEN_AUTH_GUIDE.md) - Token authentication guide
- [SWAGGER_GUIDE.md](app/SWAGGER_GUIDE.md) - Swagger UI usage guide
- [CUSTOMER_COMPANY_MODELS.md](app/CUSTOMER_COMPANY_MODELS.md) - Model relationships
- [ITEM_CUSTOMER_RELATIONSHIP.md](app/ITEM_CUSTOMER_RELATIONSHIP.md) - Item-Customer relationship

## Development

### Running Tests
```bash
python manage.py test
```

### Creating Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### Accessing Admin Panel
1. Create a superuser: `python manage.py createsuperuser`
2. Visit http://localhost:8000/admin/
3. Login with superuser credentials

### Adding Dependencies
```bash
# Add a new dependency
uv add package-name

# Sync dependencies
uv sync
```

## Environment Variables

Create a `.env` file in the project root for sensitive settings:

```env
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

## Security Notes

- Change `SECRET_KEY` in production
- Set `DEBUG=False` in production
- Configure `ALLOWED_HOSTS` for your domain
- Set `ACCOUNT_EMAIL_VERIFICATION='mandatory'` in production
- Use HTTPS in production
- Configure proper CORS settings if needed

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests
5. Submit a pull request

## License

MIT License - See LICENSE file for details

## Support

For issues and questions:
- Check the documentation files in `/app/`
- Review the Swagger UI at `/api/docs/`
- Check Django and DRF documentation
- Review django-allauth documentation
