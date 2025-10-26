# Console App - Web Interface

The `console` app handles all web-based user interface pages (non-API views).

## Purpose

This app is separate from the `api` app to maintain clean separation of concerns:
- **`api` app**: REST API endpoints, serializers, and API-related logic
- **`console` app**: Web pages, HTML templates, and browser-based user interface

## Files

### `views.py`
Contains view functions for rendering HTML pages:
- `home()` - Landing page at `/`
- `dashboard()` - User dashboard at `/dashboard/` (requires login)

### `urls.py`
URL routing for web pages:
- `/` - Home page
- `/dashboard/` - Dashboard page

## Integration

The console app integrates with the `api` app by:
- Importing models from `api.models` (Customer model)
- Using the same authentication system
- Sharing templates from `app/templates/`

## Templates

Templates are located in `/app/templates/`:
- `base.html` - Base template with navigation
- `home.html` - Landing page
- `dashboard.html` - User dashboard
- `account/login.html` - Login page (django-allauth)
- `account/signup.html` - Signup page (django-allauth)

## Usage

The console app is automatically included when you access:
- http://localhost:8000/ (home page)
- http://localhost:8000/dashboard/ (dashboard, requires login)

## Development

To add new web pages:

1. Create a view function in `console/views.py`
2. Add a URL pattern in `console/urls.py`
3. Create a template in `app/templates/`

Example:
```python
# In console/views.py
def new_page(request):
    return render(request, 'new_page.html')

# In console/urls.py
urlpatterns = [
    # ... existing patterns
    path('new/', views.new_page, name='new_page'),
]
```

Then create `app/templates/new_page.html`.
