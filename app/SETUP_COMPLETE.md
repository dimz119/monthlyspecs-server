# MonthlySpecs Server - Complete Setup Summary

## ✅ What Has Been Implemented

### 1. Django REST Framework API
- Complete REST API with CRUD operations
- Token-based authentication for API access
- Comprehensive serializers for all models
- ViewSets with custom actions for relationship management

### 2. Data Models
- **Customer**: OneToOne with User, includes phone, address, bio, profile picture
- **Company**: Business entities with contact information
- **Item**: Products/items with descriptions
- **Relationships**:
  - Customer ↔ Company (Many-to-Many)
  - Customer ↔ Item (Many-to-Many)

### 3. Web Authentication (django-allauth)
- User signup page at `/accounts/signup/`
- User login page at `/accounts/login/`
- User logout at `/accounts/logout/`
- Dashboard at `/dashboard/` (requires login)
- Home/landing page at `/`
- **Automatic Customer Profile Creation** via Django signals

### 4. Interactive API Documentation
- Swagger UI at `/api/docs/`
- ReDoc at `/api/redoc/`
- OpenAPI 3.0 schema at `/api/schema/`
- Persistent token authorization in Swagger UI

### 5. Admin Panel
- Full admin interface configured for all models
- Search functionality
- Filters for easy data management
- Many-to-Many field widgets

### 6. Templates
- Base template with navigation and styling
- Home page with feature highlights
- Dashboard showing user and customer information
- Custom login page
- Custom signup page
- Responsive design with clean CSS

### 7. Signals
- Automatic Customer profile creation on User signup
- Signal handler in `api/signals.py`
- Registered in `api/apps.py`

## 📁 File Structure

```
monthlyspecs-server/
├── app/
│   ├── api/
│   │   ├── __init__.py
│   │   ├── admin.py              # Admin panel configuration
│   │   ├── apps.py               # App configuration with signal registration
│   │   ├── models.py             # Customer, Company, Item models
│   │   ├── serializers.py        # DRF serializers
│   │   ├── signals.py            # Auto-create Customer on User creation
│   │   ├── urls.py               # API URL routing
│   │   ├── views.py              # API viewsets
│   │   ├── web_urls.py           # Web page URLs
│   │   └── web_views.py          # Web page views (home, dashboard)
│   ├── app/
│   │   ├── __init__.py
│   │   ├── settings.py           # Django settings (updated with allauth)
│   │   ├── urls.py               # Main URL configuration
│   │   ├── wsgi.py
│   │   └── asgi.py
│   ├── templates/
│   │   ├── base.html             # Base template with header/nav
│   │   ├── home.html             # Landing page
│   │   ├── dashboard.html        # User dashboard
│   │   └── account/
│   │       ├── login.html        # Custom login page
│   │       └── signup.html       # Custom signup page
│   ├── manage.py
│   ├── db.sqlite3
│   ├── API_GUIDE.md
│   ├── SWAGGER_GUIDE.md
│   ├── TOKEN_AUTH_GUIDE.md
│   ├── CUSTOMER_COMPANY_MODELS.md
│   ├── ITEM_CUSTOMER_RELATIONSHIP.md
│   └── WEB_AUTH_GUIDE.md         # NEW: Web authentication guide
├── pyproject.toml                # Updated with django-allauth
├── uv.lock
├── .gitignore
└── README.md                      # Updated with complete documentation
```

## 🔑 Key Configuration Changes

### settings.py Updates

1. **INSTALLED_APPS**: Added django.contrib.sites, allauth, allauth.account, allauth.socialaccount
2. **SITE_ID**: Set to 1 (required for django.contrib.sites)
3. **MIDDLEWARE**: Added `allauth.account.middleware.AccountMiddleware`
4. **TEMPLATES**: Added `BASE_DIR / 'templates'` to DIRS
5. **AUTHENTICATION_BACKENDS**: Added both ModelBackend and AuthenticationBackend
6. **Allauth Settings**:
   - `ACCOUNT_LOGIN_METHODS = {'username', 'email'}`
   - `ACCOUNT_SIGNUP_FIELDS` - Required fields
   - `ACCOUNT_EMAIL_VERIFICATION = 'optional'`
   - `LOGIN_REDIRECT_URL = '/dashboard/'`
   - `LOGOUT_REDIRECT_URL = '/'`

### urls.py Updates

Added:
- `path('accounts/', include('allauth.urls'))` - django-allauth URLs
- `path('', include('api.web_urls'))` - Web page URLs (home, dashboard)

## 🚀 How to Use

### Starting the Server

```bash
cd /Users/seungjoonlee/git/monthlyspecs-server
source .venv/bin/activate
cd app
python manage.py runserver
```

### Creating Your First Account

1. Visit http://localhost:8000/
2. Click "Sign Up"
3. Fill in username, email, password
4. Submit → Automatically redirected to dashboard
5. Customer profile is **automatically created**!

### Getting an API Token

**Method 1: curl**
```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "YOUR_USERNAME", "password": "YOUR_PASSWORD"}'
```

**Method 2: Swagger UI**
1. Go to http://localhost:8000/api/docs/
2. Find `/api/auth/login/`
3. Click "Try it out"
4. Enter credentials
5. Execute
6. Copy token from response

### Using the API

```bash
# List customers
curl http://localhost:8000/api/customers/ \
  -H "Authorization: Token YOUR_TOKEN"

# Create a company
curl -X POST http://localhost:8000/api/companies/ \
  -H "Authorization: Token YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name": "Acme Corp", "email": "contact@acme.com"}'
```

## 📚 Available URLs

### Web Pages (Browser)
- `/` - Home page
- `/accounts/signup/` - Sign up
- `/accounts/login/` - Login
- `/accounts/logout/` - Logout
- `/dashboard/` - Dashboard (requires login)
- `/admin/` - Admin panel

### API Endpoints (Token Required)
- `/api/auth/login/` - Get token
- `/api/companies/` - Companies CRUD
- `/api/customers/` - Customers CRUD
- `/api/items/` - Items CRUD
- `/api/users/` - Users list

### Documentation
- `/api/docs/` - Swagger UI
- `/api/redoc/` - ReDoc
- `/api/schema/` - OpenAPI schema

## 🎯 What Happens on Signup

1. User fills signup form
2. django-allauth creates User account
3. Django `post_save` signal fires
4. Signal handler in `api/signals.py` creates Customer profile
5. Customer is linked to User via OneToOne
6. User is redirected to `/dashboard/`
7. Dashboard displays User and Customer info

## 🔐 Two Authentication Systems

### Web Authentication (Sessions)
- Uses Django sessions and cookies
- For browser-based access
- Login at `/accounts/login/`
- Automatic session management

### API Token Authentication
- Uses Authorization header: `Token <key>`
- For programmatic API access
- Get token at `/api/auth/login/`
- Include in all API requests

**Important**: These are independent! Web login doesn't give you an API token.

## 📖 Documentation

All documentation is in the `app/` directory:

1. **WEB_AUTH_GUIDE.md** - Web authentication (NEW!)
   - How signup/login works
   - Automatic Customer profile creation
   - Dashboard usage
   - Troubleshooting

2. **API_GUIDE.md** - Complete API reference
   - All endpoints
   - Request/response examples
   - Authentication

3. **TOKEN_AUTH_GUIDE.md** - Token authentication
   - How to get tokens
   - Token format (must include "Token" prefix!)
   - Common issues

4. **SWAGGER_GUIDE.md** - Swagger UI usage
   - How to authenticate
   - Testing endpoints
   - Persistent authorization

5. **CUSTOMER_COMPANY_MODELS.md** - Customer-Company relationship
   - Model structure
   - Relationship management
   - API examples

6. **ITEM_CUSTOMER_RELATIONSHIP.md** - Item-Customer relationship
   - Model structure
   - Relationship management
   - API examples

## 🧪 Testing

The server is currently running and tested:
- ✅ Home page loads
- ✅ Login page loads
- ✅ Signup page loads
- ✅ Dashboard loads (after login)
- ✅ Swagger UI loads
- ✅ API schema generates
- ✅ Logout redirects correctly

## 🔧 Dependencies Installed

```toml
[project.dependencies]
django = ">=5.2.7"
djangorestframework = ">=3.16.1"
django-filter = ">=25.0"
markdown = ">=3.7"
drf-spectacular = ">=0.28.0"
django-allauth = ">=65.3.0"  # NEW!
```

## 🎉 Complete Features

- ✅ REST API with CRUD operations
- ✅ Token authentication for API
- ✅ Web authentication (login/signup)
- ✅ Automatic Customer profile creation
- ✅ Dashboard for users
- ✅ Many-to-Many relationships
- ✅ Custom actions for relationship management
- ✅ Swagger UI documentation
- ✅ Admin panel configuration
- ✅ Custom HTML templates
- ✅ Signal handlers
- ✅ Comprehensive documentation

## 🚧 Possible Future Enhancements

1. **Email Verification**: Set `ACCOUNT_EMAIL_VERIFICATION='mandatory'`
2. **Social Authentication**: Configure OAuth providers
3. **Profile Editing**: Add forms to edit Customer profile
4. **Password Reset**: Test password reset flow
5. **Email Backend**: Configure SMTP for production
6. **Profile Pictures**: Implement file upload handling
7. **Permissions**: Add custom permissions for different user types
8. **Tests**: Add unit and integration tests
9. **API Rate Limiting**: Implement throttling
10. **Production Settings**: Configure for deployment

## 📞 Support

Refer to the documentation files for detailed information on each feature. The Swagger UI at `/api/docs/` provides interactive testing of all API endpoints.

---

**Status**: ✅ Fully functional and ready to use!
**Server**: Running at http://127.0.0.1:8000/
**Last Updated**: October 26, 2025
