# Quick Start Guide - MonthlySpecs Server

## 🎯 The Essentials

Your Django REST Framework API with web authentication is **ready to use**!

### What You Have

1. **Web Interface** - Login, signup, and dashboard pages
2. **REST API** - Full CRUD operations with token authentication
3. **Automatic Features** - Customer profiles created automatically on signup
4. **Documentation** - Interactive Swagger UI for API testing

---

## 🚀 Getting Started (3 Steps)

### Step 1: Start the Server

```bash
cd /Users/seungjoonlee/git/monthlyspecs-server
source .venv/bin/activate
cd app
python manage.py runserver
```

Server starts at: **http://localhost:8000/**

### Step 2: Create an Account

1. Open browser: **http://localhost:8000/**
2. Click **"Sign Up"**
3. Enter:
   - Username: `testuser`
   - Email: `test@example.com`
   - Password: `testpass123`
   - Password (again): `testpass123`
4. Click **"Sign Up"**
5. You're automatically logged in and redirected to dashboard!

**What happened?**
- ✅ User account created
- ✅ Customer profile **automatically created** (via Django signals!)
- ✅ Session started (you're logged in)
- ✅ Redirected to dashboard

### Step 3: Get Your API Token

**Option A: Using Swagger UI (Easiest)**

1. Go to **http://localhost:8000/api/docs/**
2. Find `/api/auth/login/` endpoint
3. Click **"Try it out"**
4. Enter your credentials:
   ```json
   {
     "username": "testuser",
     "password": "testpass123"
   }
   ```
5. Click **"Execute"**
6. Copy the token from the response
7. Click **"Authorize"** button at the top
8. Paste token (without "Token" prefix)
9. Click **"Authorize"**
10. Now you can test all API endpoints!

**Option B: Using curl**

```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "testuser", "password": "testpass123"}'
```

Response:
```json
{
  "token": "abc123def456...",
  "user_id": 1,
  "username": "testuser",
  "email": "test@example.com",
  "auth_header": "Token abc123def456..."
}
```

Use the `auth_header` value for API calls!

---

## 🎮 Try It Out

### Test the Web Interface

1. **Home Page**: http://localhost:8000/
2. **Dashboard**: http://localhost:8000/dashboard/
3. **Logout**: http://localhost:8000/accounts/logout/
4. **Login Again**: http://localhost:8000/accounts/login/

### Test the API

**List all customers:**
```bash
curl http://localhost:8000/api/customers/ \
  -H "Authorization: Token YOUR_TOKEN_HERE"
```

**Create a company:**
```bash
curl -X POST http://localhost:8000/api/companies/ \
  -H "Authorization: Token YOUR_TOKEN_HERE" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Acme Corporation",
    "email": "contact@acme.com",
    "phone": "555-1234",
    "address": "123 Main Street, Suite 100"
  }'
```

**Add company to customer:**
```bash
# Replace {customer_id} and {company_id} with actual IDs
curl -X POST http://localhost:8000/api/customers/{customer_id}/add_company/ \
  -H "Authorization: Token YOUR_TOKEN_HERE" \
  -H "Content-Type: application/json" \
  -d '{"company_id": {company_id}}'
```

### Use Swagger UI (Interactive Testing)

1. Go to **http://localhost:8000/api/docs/**
2. Click **"Authorize"** button
3. Enter your token
4. Try any endpoint - just click and execute!

---

## 📍 Important URLs

### Web Pages (Use Browser)
- **Home**: http://localhost:8000/
- **Signup**: http://localhost:8000/accounts/signup/
- **Login**: http://localhost:8000/accounts/login/
- **Dashboard**: http://localhost:8000/dashboard/
- **Admin**: http://localhost:8000/admin/

### API Endpoints (Use Token)
- **Get Token**: `POST /api/auth/login/`
- **Companies**: `/api/companies/`
- **Customers**: `/api/customers/`
- **Items**: `/api/items/`
- **Users**: `/api/users/`

### Documentation
- **Swagger UI**: http://localhost:8000/api/docs/
- **ReDoc**: http://localhost:8000/api/redoc/

---

## 💡 Key Concepts

### Two Authentication Systems

**Web Authentication** (Sessions):
- For browser access
- Login at `/accounts/login/`
- Uses cookies
- Automatic after signup

**API Authentication** (Tokens):
- For API access
- Get token at `/api/auth/login/`
- Use `Authorization: Token <key>` header
- Required for all API calls

**Important**: They're separate! Web login ≠ API token

### Customer Profile Auto-Creation

When you sign up:
1. User account is created by django-allauth
2. Django signal triggers automatically
3. Customer profile is created and linked to User
4. All happens in the background!

Check the signal code in `app/api/signals.py`:
```python
@receiver(post_save, sender=User)
def create_customer_profile(sender, instance, created, **kwargs):
    if created:
        Customer.objects.create(user=instance)
```

---

## 📚 Need More Help?

### Documentation Files (in `app/` directory)

1. **WEB_AUTH_GUIDE.md** - Web authentication details
2. **API_GUIDE.md** - Complete API reference
3. **TOKEN_AUTH_GUIDE.md** - Token authentication
4. **SWAGGER_GUIDE.md** - Swagger UI usage
5. **CUSTOMER_COMPANY_MODELS.md** - Customer-Company relationships
6. **ITEM_CUSTOMER_RELATIONSHIP.md** - Item-Customer relationships
7. **SETUP_COMPLETE.md** - Full setup summary

### Common Issues

**Can't login on website?**
- Make sure you created an account at `/accounts/signup/`
- Try password reset at `/accounts/password/reset/`

**API returns 401 Unauthorized?**
- Check you're using correct token
- Make sure header format is: `Authorization: Token <key>`
- Verify token is still valid (doesn't expire by default)

**Customer profile doesn't exist?**
- Signals should create it automatically
- Check admin panel at `/admin/api/customer/`
- Can create manually via API or admin

**Token format error?**
- Must be: `Token abc123...` (with "Token" prefix!)
- Not: `Bearer abc123...`
- Not: `abc123...`

---

## 🎉 You're Ready!

Your application is fully set up with:
- ✅ Web authentication (login/signup)
- ✅ API with token authentication
- ✅ Automatic customer profile creation
- ✅ Interactive API documentation
- ✅ Dashboard for users
- ✅ Full CRUD operations
- ✅ Many-to-Many relationships

**Start building your application!** 🚀

---

## 🔧 Admin Access (Optional)

To access the admin panel:

```bash
python manage.py createsuperuser
```

Then visit: **http://localhost:8000/admin/**

---

**Need help?** Check the documentation files or the Swagger UI for details!
