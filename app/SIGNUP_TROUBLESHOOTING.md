# Signup Troubleshooting Guide

## Issue Fixed: Signup Form Not Working

### What Was Wrong

1. **Settings Configuration Error**: The allauth settings had invalid configuration that caused the server to crash
2. **Form Errors Not Displayed**: Custom templates weren't showing validation errors

### What Was Fixed

1. **Removed Invalid Settings**:
   - Removed `ACCOUNT_LOGIN_METHODS` (conflicted with other settings)
   - Removed `ACCOUNT_SIGNUP_FIELDS` (had invalid format)
   - Kept only the essential allauth settings

2. **Updated Templates**:
   - Added error display blocks to `signup.html` and `login.html`
   - Now shows field-specific errors
   - Shows non-field errors (like username already exists)
   - Preserves form values on error

### Current Working Settings

```python
# Authentication Backends
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

# Django-allauth settings
ACCOUNT_EMAIL_VERIFICATION = 'optional'
LOGIN_REDIRECT_URL = '/dashboard/'
LOGOUT_REDIRECT_URL = '/'
ACCOUNT_LOGOUT_ON_GET = True
```

## How to Test Signup

### 1. Visit Signup Page
http://localhost:8000/accounts/signup/

### 2. Fill Out the Form

**Valid Example:**
- Username: `testuser`
- Email: `test@example.com`
- Password: `mypassword123`
- Password (again): `mypassword123`

**Important Password Rules:**
- At least 8 characters long
- Can't be too similar to username or email
- Can't be entirely numeric
- Can't be a common password (like "password123")

### 3. Submit

If successful:
- ✅ User account created
- ✅ Customer profile auto-created (via signal)
- ✅ Logged in automatically
- ✅ Redirected to `/dashboard/`

If there are errors:
- ❌ Form shows specific error messages
- ❌ Form values are preserved
- ❌ You can correct and resubmit

## Common Signup Errors

### "This password is too common"
**Solution**: Use a more unique password, like `MySecurePass2024!`

### "This password is too short"
**Solution**: Use at least 8 characters

### "This password is entirely numeric"
**Solution**: Include letters in your password

### "A user with that username already exists"
**Solution**: Choose a different username

### "Enter a valid email address"
**Solution**: Make sure email has proper format (user@domain.com)

### "The two password fields didn't match"
**Solution**: Make sure both password fields are exactly the same

## Verify Signup Worked

### Check Dashboard
After signup, you should be at: http://localhost:8000/dashboard/

You should see:
- Your username
- Your email
- Customer profile information (automatically created!)

### Check Admin Panel

1. Go to http://localhost:8000/admin/
2. Login with your new account (if you made a superuser)
3. Navigate to "Users" - you should see your new user
4. Navigate to "Customers" - you should see your Customer profile

### Check Database via Django Shell

```bash
python manage.py shell
```

```python
from django.contrib.auth.models import User
from api.models import Customer

# Check if user exists
user = User.objects.get(username='testuser')
print(f"User: {user.username}, Email: {user.email}")

# Check if customer profile exists
customer = Customer.objects.get(user=user)
print(f"Customer ID: {customer.id}, Created: {customer.created_at}")
```

## How the Auto Customer Creation Works

When you sign up:

1. **django-allauth creates User**
   ```python
   user = User.objects.create(username='testuser', email='test@example.com')
   ```

2. **Django Signal Fires**
   ```python
   # In api/signals.py
   @receiver(post_save, sender=User)
   def create_customer_profile(sender, instance, created, **kwargs):
       if created:
           Customer.objects.create(user=instance)
   ```

3. **Customer Profile Created**
   ```python
   customer = Customer.objects.create(user=user)
   ```

4. **OneToOne Link Established**
   - `user.customer` → Customer instance
   - `customer.user` → User instance

## Test the Full Flow

### 1. Sign Up
```
Visit: http://localhost:8000/accounts/signup/
Fill: username=newuser, email=new@test.com, password=TestPass123!
Submit → Should redirect to dashboard
```

### 2. Check Dashboard
```
URL should be: http://localhost:8000/dashboard/
Should show: User info + Customer profile
```

### 3. Logout
```
Click "Logout" in navigation
Should redirect to: http://localhost:8000/
```

### 4. Login Again
```
Visit: http://localhost:8000/accounts/login/
Fill: username=newuser (or email), password=TestPass123!
Submit → Should redirect to dashboard again
```

### 5. Get API Token
```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "newuser", "password": "TestPass123!"}'
```

Should return:
```json
{
  "token": "abc123...",
  "user_id": 1,
  "username": "newuser",
  "email": "new@test.com",
  "auth_header": "Token abc123..."
}
```

### 6. Use API
```bash
curl http://localhost:8000/api/customers/ \
  -H "Authorization: Token abc123..."
```

Should show your customer profile!

## Still Having Issues?

### Check Server Logs
The terminal running `python manage.py runserver` shows all requests and errors.

Look for:
- `POST /accounts/signup/ HTTP/1.1 200` - Form validation error (shows signup page again)
- `POST /accounts/signup/ HTTP/1.1 302` - Success! (redirects to dashboard)
- Any Python tracebacks or error messages

### Debug in Browser
1. Open browser developer tools (F12)
2. Go to Network tab
3. Try signup again
4. Check the POST request to `/accounts/signup/`
5. Look at the response - may contain error details

### Manual User Creation
If signup still doesn't work, create user manually:

```bash
python manage.py createsuperuser
```

Then:
1. Visit http://localhost:8000/admin/
2. Login with superuser
3. Create a Customer profile manually for the user

## Summary

✅ **Fixed Issues:**
- Invalid allauth settings removed
- Templates now show form errors
- Server runs without crashes

✅ **What Works:**
- Signup form displays properly
- Validation errors are shown
- Successful signups redirect to dashboard
- Customer profiles auto-created via signals
- Login/logout works
- Dashboard shows user and customer info

🎉 **Your authentication system is ready to use!**
