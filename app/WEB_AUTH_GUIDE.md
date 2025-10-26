# Web Authentication Setup Guide

This guide explains how to use the web-based authentication (login/signup) feature alongside the API token authentication.

## Two Authentication Systems

This application has **two independent authentication systems**:

1. **Web Authentication** (django-allauth) - For browser-based access
2. **API Token Authentication** - For programmatic API access

### Web Authentication (Browser-based)

Used for:
- Logging into the web interface
- Accessing the dashboard
- Managing your profile through the web UI

### API Token Authentication

Used for:
- Programmatic API access (curl, Postman, etc.)
- Client applications making API calls
- Swagger UI testing

## Getting Started

### 1. Sign Up for a New Account

Visit: `http://localhost:8000/accounts/signup/`

Fill in:
- Username
- Email
- Password
- Password confirmation

When you sign up:
- A User account is created
- A Customer profile is **automatically created** for you (via Django signals)
- You're redirected to the dashboard at `/dashboard/`

### 2. Login to Existing Account

Visit: `http://localhost:8000/accounts/login/`

You can login with:
- Your username
- Your email address

### 3. View Your Dashboard

After login, visit: `http://localhost:8000/dashboard/`

The dashboard shows:
- Your user information
- Your customer profile details
- Associated companies
- Quick links to API documentation

## URL Structure

### Web Pages (Browser Access)

- `/` - Home page (landing page)
- `/accounts/signup/` - Sign up page
- `/accounts/login/` - Login page
- `/accounts/logout/` - Logout (redirects to home)
- `/dashboard/` - Dashboard (requires login)
- `/admin/` - Django admin panel

### API Endpoints (Token Authentication Required)

- `/api/auth/login/` - Get API token (POST username & password)
- `/api/companies/` - Company CRUD endpoints
- `/api/customers/` - Customer CRUD endpoints
- `/api/items/` - Item CRUD endpoints
- `/api/users/` - User CRUD endpoints

### Documentation

- `/api/docs/` - Swagger UI (interactive API docs)
- `/api/schema/` - OpenAPI schema (JSON)
- `/api/redoc/` - ReDoc documentation

## Automatic Customer Profile Creation

When a new user signs up through the web interface:

1. User account is created by django-allauth
2. A Django signal (`post_save` on User model) triggers
3. A Customer profile is automatically created
4. The Customer profile is linked to the User via OneToOne relationship

This is handled by the signal in `api/signals.py`:

```python
@receiver(post_save, sender=User)
def create_customer_profile(sender, instance, created, **kwargs):
    if created:
        Customer.objects.create(user=instance)
```

## Testing the Authentication Flow

### Test Web Authentication

1. **Visit the home page**: `http://localhost:8000/`
2. **Click "Sign Up"**
3. **Create an account** with:
   - Username: testuser
   - Email: test@example.com
   - Password: testpass123
   - Password confirmation: testpass123
4. **You're redirected to dashboard** automatically
5. **Check your profile** - should see User info and Customer profile

### Test API Authentication

1. **Get your API token**:
   ```bash
   curl -X POST http://localhost:8000/api/auth/login/ \
     -H "Content-Type: application/json" \
     -d '{"username": "testuser", "password": "testpass123"}'
   ```

2. **Response includes your token**:
   ```json
   {
     "token": "abc123...",
     "user_id": 1,
     "username": "testuser",
     "email": "test@example.com",
     "auth_header": "Token abc123..."
   }
   ```

3. **Use the token for API calls**:
   ```bash
   curl http://localhost:8000/api/customers/ \
     -H "Authorization: Token abc123..."
   ```

## Important Notes

### Session vs Token

- **Web interface** uses Django sessions (cookie-based)
- **API calls** use Token authentication (header-based)
- These are **independent** - logging in on the web doesn't give you an API token

### Getting an API Token

After creating a web account, you need to:

1. **Option A**: Use the `/api/auth/login/` endpoint (see above)
2. **Option B**: Use Swagger UI at `/api/docs/`
   - Click "Authorize" button
   - Click "Execute" on `/api/auth/login/`
   - Enter username and password
   - Copy the token from response

### Customer Profile Fields

The automatically created Customer profile includes:
- `user` - OneToOne link to User
- `phone` - Phone number (optional)
- `address` - Address (optional)
- `date_of_birth` - Date of birth (optional)
- `bio` - Biography (optional)
- `profile_picture` - Profile image (optional)
- `companies` - Many-to-Many relationship to Company
- `created_at` - Creation timestamp
- `updated_at` - Last update timestamp

You can update these fields through:
- The API using your token
- The Django admin panel
- Custom forms (to be implemented)

## Configuration

### Key Settings (in `app/settings.py`)

```python
# Allow login with username or email
ACCOUNT_LOGIN_METHODS = {'username', 'email'}

# Required signup fields
ACCOUNT_SIGNUP_FIELDS = [
    'email*',
    'username*',
    'password1*',
    'password2*',
]

# Email verification (set to 'mandatory' in production)
ACCOUNT_EMAIL_VERIFICATION = 'optional'

# Redirect after login
LOGIN_REDIRECT_URL = '/dashboard/'

# Redirect after logout
LOGOUT_REDIRECT_URL = '/'
```

### Authentication Backends

Both authentication methods are configured:

```python
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',  # For web login
    'allauth.account.auth_backends.AuthenticationBackend',  # For allauth
]
```

## Troubleshooting

### Customer Profile Not Created

If a user somehow doesn't have a Customer profile:

**Option 1**: Create via Django admin
- Go to `/admin/`
- Click "Customers" → "Add customer"
- Select the user and save

**Option 2**: Create via API
```bash
curl -X POST http://localhost:8000/api/customers/ \
  -H "Authorization: Token YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"username": "existinguser", "email": "user@example.com", "password": "pass123"}'
```

### Can't Login to Web Interface

- Make sure you're using the correct username/email and password
- Check if the user exists in `/admin/auth/user/`
- Try password reset at `/accounts/password/reset/`

### Can't Get API Token

- Verify username and password are correct
- Make sure the user exists (check admin panel)
- Use the exact endpoint: `/api/auth/login/` (not `/accounts/login/`)

## Next Steps

Now that you have authentication set up:

1. **Customize the dashboard** - Add more customer information
2. **Add profile editing** - Let users update their Customer profile
3. **Implement email verification** - Set `ACCOUNT_EMAIL_VERIFICATION = 'mandatory'`
4. **Add social authentication** - Configure providers in `allauth.socialaccount`
5. **Add permissions** - Control who can access what data

## Related Documentation

- [API_GUIDE.md](API_GUIDE.md) - Complete API documentation
- [TOKEN_AUTH_GUIDE.md](TOKEN_AUTH_GUIDE.md) - Token authentication details
- [SWAGGER_GUIDE.md](SWAGGER_GUIDE.md) - Using Swagger UI
- [CUSTOMER_COMPANY_MODELS.md](CUSTOMER_COMPANY_MODELS.md) - Model relationships
