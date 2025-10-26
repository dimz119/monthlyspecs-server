# Swagger/OpenAPI Documentation Guide

## 🎉 Swagger UI is Now Available!

Your Django REST Framework API now includes interactive API documentation powered by **drf-spectacular**.

## 📍 Access Points

Once your server is running (`python manage.py runserver`), you can access:

### Swagger UI (Recommended)
**URL:** http://localhost:8000/api/docs/

Interactive API documentation with a user-friendly interface where you can:
- Browse all available endpoints
- View request/response schemas
- Test API calls directly from the browser
- Authenticate using your token

### ReDoc (Alternative UI)
**URL:** http://localhost:8000/api/redoc/

A clean, three-panel API documentation interface that's great for reading and sharing.

### OpenAPI Schema (Raw JSON)
**URL:** http://localhost:8000/api/schema/

The raw OpenAPI 3.0 schema in JSON format. Useful for:
- Importing into API testing tools (Postman, Insomnia)
- Generating client SDKs
- Integration with other tools

## 🔐 How to Use Swagger UI with Token Authentication

### Step 1: Get Your Token
First, you need to authenticate and get a token. You can do this in two ways:

**Option A: Using the Swagger UI**
1. Go to http://localhost:8000/api/docs/
2. Find the `POST /api/auth/login/` endpoint
3. Click "Try it out"
4. Enter your credentials:
   ```json
   {
     "username": "your-username",
     "password": "your-password"
   }
   ```
5. Click "Execute"
6. Copy the token from the response

**Option B: Using curl**
```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "your-password"}'
```

### Step 2: Authorize in Swagger UI
1. Click the **"Authorize"** button at the top right of the Swagger UI
2. In the popup, enter: `Token <your-token-here>`
   - Example: `Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b`
3. Click "Authorize"
4. Click "Close"

Now all your API requests will include the authentication token! 🎉

### Step 3: Test Your APIs
- Click on any endpoint to expand it
- Click "Try it out"
- Fill in the parameters (if needed)
- Click "Execute"
- View the response

## 📋 Quick Start Checklist

1. ✅ Install drf-spectacular: `uv sync` (already done)
2. ✅ Configure settings (already done)
3. ✅ Add URL patterns (already done)
4. 🔄 Create a superuser: `python manage.py createsuperuser`
5. 🔄 Start the server: `python manage.py runserver`
6. 🔄 Visit http://localhost:8000/api/docs/
7. 🔄 Login and get your token
8. 🔄 Click "Authorize" and enter your token
9. 🔄 Start testing your APIs!

## 🎨 Customization

The Swagger UI is configured in `app/settings.py` under `SPECTACULAR_SETTINGS`. You can customize:

```python
SPECTACULAR_SETTINGS = {
    'TITLE': 'MonthlySpecs API',  # Change this to your project name
    'DESCRIPTION': 'API documentation for MonthlySpecs Server',
    'VERSION': '1.0.0',
    # ... more settings
}
```

## 📚 Available Endpoints

After setup, you'll see these endpoints in Swagger:

### Authentication
- `POST /api/auth/login/` - Login and receive token
- `POST /api/auth/logout/` - Logout (requires auth)

### Items
- `GET /api/items/` - List all items
- `POST /api/items/` - Create new item
- `GET /api/items/{id}/` - Get item details
- `PUT /api/items/{id}/` - Full update
- `PATCH /api/items/{id}/` - Partial update
- `DELETE /api/items/{id}/` - Delete item

### Users
- `GET /api/users/` - List all users
- `GET /api/users/{id}/` - Get user details

## 💡 Tips & Tricks

### 1. Export OpenAPI Schema
Download the schema for use in other tools:
```bash
curl http://localhost:8000/api/schema/ -o openapi-schema.json
```

### 2. Import to Postman
1. Open Postman
2. Click "Import"
3. Enter URL: `http://localhost:8000/api/schema/`
4. All endpoints will be imported automatically!

### 3. Generate Client SDK
Use the OpenAPI schema to generate client code:
```bash
# Install OpenAPI Generator
npm install @openapitools/openapi-generator-cli -g

# Generate Python client
openapi-generator-cli generate \
  -i http://localhost:8000/api/schema/ \
  -g python \
  -o ./client-sdk
```

### 4. Add Documentation to Your Views
Enhance the Swagger docs by adding docstrings:

```python
from drf_spectacular.utils import extend_schema, OpenApiParameter

class ItemViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing items.
    
    Provides CRUD operations for Item resources.
    """
    
    @extend_schema(
        summary="List all items",
        description="Returns a paginated list of all items",
        tags=["Items"]
    )
    def list(self, request):
        # Your code here
        pass
```

## 🚀 What's Next?

1. **Add tags to organize endpoints** - Group related endpoints together
2. **Add examples** - Provide sample request/response data
3. **Document query parameters** - Add descriptions for filters and search
4. **Add versioning** - Plan for API version management
5. **Enable CORS** - If you need to access from a frontend app

## 🔗 Useful Links

- drf-spectacular docs: https://drf-spectacular.readthedocs.io/
- OpenAPI Specification: https://swagger.io/specification/
- Django REST Framework: https://www.django-rest-framework.org/

---

**Happy API Testing! 🎊**
