# Django REST Framework API - Bootstrap Setup

This project has been configured with Django REST Framework (DRF) and Token Authentication.

## � Documentation

**Interactive API Documentation (Swagger UI):** http://localhost:8000/api/docs/

**Alternative Documentation (ReDoc):** http://localhost:8000/api/redoc/

**OpenAPI Schema:** http://localhost:8000/api/schema/

> 💡 **Tip:** Use Swagger UI for interactive testing! See [SWAGGER_GUIDE.md](SWAGGER_GUIDE.md) for details.

## �🚀 Quick Start

### 1. Create a superuser (for testing)
```bash
cd app
python manage.py createsuperuser
```

### 2. Run the development server
```bash
cd app
python manage.py runserver
```

### 3. Access Swagger UI
Open your browser and go to http://localhost:8000/api/docs/

## 🔐 Authentication

This API uses **Token Authentication**. Clients must include the token in the request header:

```
Authorization: Token <your-token-here>
```

### Getting a Token

**Login endpoint:**
```bash
POST /api/auth/login/
Content-Type: application/json

{
    "username": "your-username",
    "password": "your-password"
}
```

**Response:**
```json
{
    "token": "9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b",
    "user_id": 1,
    "username": "your-username",
    "email": "user@example.com"
}
```

**Logout endpoint:**
```bash
POST /api/auth/logout/
Authorization: Token <your-token>
```

## 📡 Available API Endpoints

### Authentication
- `POST /api/auth/login/` - Login and get token
- `POST /api/auth/logout/` - Logout (requires authentication)

### Items (Sample CRUD API)
- `GET /api/items/` - List all items
- `POST /api/items/` - Create a new item
- `GET /api/items/{id}/` - Retrieve a specific item
- `PUT /api/items/{id}/` - Update an item (full update)
- `PATCH /api/items/{id}/` - Partial update an item
- `DELETE /api/items/{id}/` - Delete an item

### Users (Read-only)
- `GET /api/users/` - List all users
- `GET /api/users/{id}/` - Retrieve a specific user

## 📝 Example API Requests

### 1. Login and get token
```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "your-password"}'
```

### 2. Create an item (with authentication)
```bash
curl -X POST http://localhost:8000/api/items/ \
  -H "Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b" \
  -H "Content-Type: application/json" \
  -d '{"name": "My First Item", "description": "This is a test item"}'
```

### 3. List all items
```bash
curl -X GET http://localhost:8000/api/items/ \
  -H "Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b"
```

### 4. Update an item
```bash
curl -X PATCH http://localhost:8000/api/items/1/ \
  -H "Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b" \
  -H "Content-Type: application/json" \
  -d '{"description": "Updated description"}'
```

### 5. Delete an item
```bash
curl -X DELETE http://localhost:8000/api/items/1/ \
  -H "Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b"
```

### 6. Logout
```bash
curl -X POST http://localhost:8000/api/auth/logout/ \
  -H "Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b"
```

## 🏗️ Project Structure

```
app/
├── api/                    # Main API app
│   ├── models.py          # Sample Item model
│   ├── serializers.py     # DRF serializers
│   ├── views.py           # API views and viewsets
│   └── urls.py            # API URL routing
├── app/
│   ├── settings.py        # Django settings (DRF configured here)
│   └── urls.py            # Main URL configuration
└── manage.py
```

## ⚙️ DRF Configuration

The following settings are configured in `app/settings.py`:

```python
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
}
```

## 🔨 Adding New APIs

### 1. Create a model in `api/models.py`
```python
class YourModel(models.Model):
    name = models.CharField(max_length=200)
    # ... add fields
```

### 2. Create a serializer in `api/serializers.py`
```python
class YourModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = YourModel
        fields = '__all__'
```

### 3. Create a viewset in `api/views.py`
```python
class YourModelViewSet(viewsets.ModelViewSet):
    queryset = YourModel.objects.all()
    serializer_class = YourModelSerializer
    permission_classes = [permissions.IsAuthenticated]
```

### 4. Register in `api/urls.py`
```python
router.register(r'yourmodels', views.YourModelViewSet, basename='yourmodel')
```

### 5. Run migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

## 🎯 Next Steps

1. Create a superuser to test the API
2. Customize the `Item` model or create your own models
3. Add custom permissions or authentication if needed
4. Consider adding API documentation with drf-spectacular or drf-yasg
5. Set up CORS if your frontend is on a different domain (install django-cors-headers)
6. Move sensitive settings to environment variables for production

## 🔒 Security Notes

- The `SECRET_KEY` in settings.py should be changed and stored in environment variables
- Set `DEBUG = False` in production
- Configure `ALLOWED_HOSTS` for production
- Use HTTPS in production
- Consider rate limiting for production (use django-ratelimit or similar)
