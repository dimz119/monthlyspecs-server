# Token Authentication - Quick Reference

## ⚠️ Common Issue: Missing "Token" Prefix

The most common authentication error is forgetting the `Token` prefix in the Authorization header.

### ❌ WRONG - This will NOT work:
```bash
curl -X GET http://127.0.0.1:8000/api/items/ \
  -H 'Authorization: d001965bba4175157d705255a5c8f2291a59286a'
```

**Error:** `"Authentication credentials were not provided."`

### ✅ CORRECT - This WILL work:
```bash
curl -X GET http://127.0.0.1:8000/api/items/ \
  -H 'Authorization: Token d001965bba4175157d705255a5c8f2291a59286a'
```

## 🔑 The Format

Django REST Framework's TokenAuthentication requires this exact format:

```
Authorization: Token <your-token-here>
```

- The word `Token` is required
- There must be a space between `Token` and your actual token
- The token is the long string you received from the login endpoint

## 📝 Step-by-Step Guide

### 1. Login to Get Your Token

```bash
curl -X POST http://127.0.0.1:8000/api/auth/login/ \
  -H 'Content-Type: application/json' \
  -d '{"username": "admin", "password": "your-password"}'
```

**Response:**
```json
{
  "token": "d001965bba4175157d705255a5c8f2291a59286a",
  "user_id": 1,
  "username": "admin",
  "email": "admin@example.com",
  "auth_header": "Token d001965bba4175157d705255a5c8f2291a59286a"
}
```

### 2. Copy the `auth_header` Value

The response now includes an `auth_header` field with the complete value you need!

### 3. Use It in Your Requests

```bash
curl -X GET http://127.0.0.1:8000/api/items/ \
  -H 'Authorization: Token d001965bba4175157d705255a5c8f2291a59286a'
```

## 🌐 Using Swagger UI

### Step 1: Login
1. Go to http://localhost:8000/api/docs/
2. Find `POST /api/auth/login/`
3. Click "Try it out"
4. Enter your credentials
5. Click "Execute"
6. Copy the `auth_header` value from the response

### Step 2: Authorize
1. Click the **"Authorize"** button (green lock icon at the top)
2. Paste the COMPLETE `auth_header` value: `Token d001965bba4175157d705255a5c8f2291a59286a`
3. Click "Authorize"
4. Click "Close"

### Step 3: Token Persistence
The token is now stored in your browser's localStorage and will persist even after page refreshes! 🎉

To logout:
- Click "Authorize" again
- Click "Logout"
- Or just clear the value and click "Authorize"

## 🧪 Testing with Different Tools

### Postman
```
Authorization: Token d001965bba4175157d705255a5c8f2291a59286a
```

### Insomnia
```
Authorization: Token d001965bba4175157d705255a5c8f2291a59286a
```

### JavaScript (fetch)
```javascript
fetch('http://127.0.0.1:8000/api/items/', {
  headers: {
    'Authorization': 'Token d001965bba4175157d705255a5c8f2291a59286a',
    'Content-Type': 'application/json'
  }
})
```

### Python (requests)
```python
import requests

headers = {
    'Authorization': 'Token d001965bba4175157d705255a5c8f2291a59286a'
}

response = requests.get('http://127.0.0.1:8000/api/items/', headers=headers)
```

## 🔄 Token Lifecycle

### Getting a Token
- Use `POST /api/auth/login/` with username and password
- One token per user (calling login again returns the same token)

### Using a Token
- Include in every API request: `Authorization: Token <token>`
- Token remains valid until explicitly deleted

### Revoking a Token
- Use `POST /api/auth/logout/` (requires authentication)
- This deletes your token
- You'll need to login again to get a new token

## 🎯 Quick Checklist

Before making an authenticated API call, verify:

- [ ] I got my token from `/api/auth/login/`
- [ ] My Authorization header starts with the word `Token`
- [ ] There's a space between `Token` and my actual token
- [ ] I'm using the complete token string (usually 40 characters)

## 💡 Pro Tips

1. **Copy from `auth_header`:** The login response now includes a ready-to-use `auth_header` field
2. **Use Swagger UI:** The "Authorize" button makes testing much easier
3. **Token Persistence:** In Swagger UI, your token is saved in browser storage
4. **Environment Variables:** Store your token in environment variables for security
5. **Testing:** Use Swagger UI for quick tests, then implement in your application

## 🐛 Troubleshooting

### "Authentication credentials were not provided"
✅ Add the `Token` prefix to your Authorization header

### "Invalid token"
✅ Make sure you're using the complete token from the login response
✅ Check if your token was deleted (try logging in again)

### Token keeps disappearing in Swagger UI
✅ Make sure `persistAuthorization: true` is set in settings (already configured)
✅ Check browser console for errors
✅ Try a different browser or clear browser cache

---

**Remember:** Always include `Token` before your actual token! 🔐
