# Authentication Flow Diagram

## Visual Overview of MonthlySpecs Server Authentication

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    MonthlySpecs Server Architecture                      │
└─────────────────────────────────────────────────────────────────────────┘

┌──────────────────────┐              ┌──────────────────────┐
│   Web Browser User   │              │   API Client (curl,  │
│                      │              │   Postman, Mobile)   │
└──────────┬───────────┘              └──────────┬───────────┘
           │                                     │
           │                                     │
           ▼                                     ▼
┌─────────────────────┐              ┌─────────────────────┐
│  WEB AUTHENTICATION │              │ API TOKEN AUTH      │
│  (django-allauth)   │              │ (DRF Token)         │
└─────────────────────┘              └─────────────────────┘
           │                                     │
           │                                     │
           ▼                                     ▼

┌───────────────────────────────────────────────────────────────────────┐
│                       SIGNUP/LOGIN FLOWS                              │
├───────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  WEB SIGNUP FLOW:                    API LOGIN FLOW:                 │
│  ────────────────                    ────────────────                │
│                                                                       │
│  1. User visits /accounts/signup/    1. POST /api/auth/login/        │
│  2. Fills form (username, email,        with username & password     │
│     password)                                                         │
│  3. Submits form                     2. Server validates credentials │
│                                                                       │
│  4. django-allauth creates User      3. Returns token:               │
│                                         {                             │
│  5. Django Signal Fires! 🔔             "token": "abc123...",        │
│     post_save(User)                     "auth_header": "Token ..."   │
│                                         }                             │
│  6. Signal Handler in                                                │
│     api/signals.py:                  4. Client stores token          │
│     - Creates Customer profile                                       │
│     - Links to User (OneToOne)       5. Client includes token in     │
│                                         all API requests:             │
│  7. User logged in (session)            Authorization: Token abc123  │
│                                                                       │
│  8. Redirected to /dashboard/        6. Server validates token       │
│                                                                       │
│  9. Dashboard shows:                 7. Returns requested data        │
│     - User info                                                       │
│     - Customer profile ✅                                             │
│     - Companies                                                       │
│                                                                       │
└───────────────────────────────────────────────────────────────────────┘


┌───────────────────────────────────────────────────────────────────────┐
│                          DATA MODELS                                  │
├───────────────────────────────────────────────────────────────────────┤
│                                                                       │
│   User (Django Auth)                                                  │
│   ├── username                                                        │
│   ├── email                                                           │
│   ├── password                                                        │
│   └── Customer (OneToOne) ──┐                                        │
│                               │                                       │
│   Customer                    │                                       │
│   ├── user ◄─────────────────┘                                       │
│   ├── phone                                                           │
│   ├── address                                                         │
│   ├── date_of_birth                                                   │
│   ├── bio                                                             │
│   ├── profile_picture                                                 │
│   ├── companies (M2M) ──────────┐                                    │
│   └── items (M2M) ───────┐      │                                    │
│                           │      │                                    │
│   Company                 │      │                                    │
│   ├── name                │      │                                    │
│   ├── email               │      │                                    │
│   ├── phone               │      │                                    │
│   ├── address             │      │                                    │
│   └── customers ◄─────────┘      │                                    │
│                                   │                                    │
│   Item                            │                                    │
│   ├── name                        │                                    │
│   ├── description                 │                                    │
│   └── customers ◄─────────────────┘                                    │
│                                                                       │
└───────────────────────────────────────────────────────────────────────┘


┌───────────────────────────────────────────────────────────────────────┐
│                      URL ROUTING                                      │
├───────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  WEB URLS (Browser):              API URLS (Token):                  │
│  ──────────────────               ─────────────────                  │
│                                                                       │
│  /                                /api/                              │
│  └── home.html                    ├── auth/                          │
│                                   │   ├── login/                      │
│  /accounts/                       │   └── logout/                     │
│  ├── signup/                      │                                   │
│  ├── login/                       ├── companies/                      │
│  ├── logout/                      │   ├── [list]                      │
│  └── password/reset/              │   ├── {id}/                       │
│                                   │   ├── {id}/add_customer/          │
│  /dashboard/                      │   └── {id}/customers/             │
│  └── dashboard.html               │                                   │
│                                   ├── customers/                      │
│  /admin/                          │   ├── [list]                      │
│  └── Django Admin                 │   ├── {id}/                       │
│                                   │   ├── {id}/add_company/           │
│                                   │   └── {id}/add_item/              │
│  /api/docs/                       │                                   │
│  └── Swagger UI                   ├── items/                          │
│                                   │   ├── [list]                      │
│                                   │   ├── {id}/                       │
│                                   │   └── {id}/add_customer/          │
│                                   │                                   │
│                                   └── users/                          │
│                                       └── [list]                      │
│                                                                       │
└───────────────────────────────────────────────────────────────────────┘


┌───────────────────────────────────────────────────────────────────────┐
│                   SIGNAL HANDLER FLOW                                 │
├───────────────────────────────────────────────────────────────────────┤
│                                                                       │
│   User Signs Up                                                       │
│        │                                                              │
│        ▼                                                              │
│   django-allauth creates User                                         │
│        │                                                              │
│        ▼                                                              │
│   User.save() called                                                  │
│        │                                                              │
│        ▼                                                              │
│   post_save signal fires                                              │
│        │                                                              │
│        ▼                                                              │
│   @receiver in api/signals.py triggered                               │
│        │                                                              │
│        ▼                                                              │
│   if created == True:                                                 │
│        │                                                              │
│        ▼                                                              │
│   Customer.objects.create(user=instance)                              │
│        │                                                              │
│        ▼                                                              │
│   Customer profile created! ✅                                         │
│        │                                                              │
│        ▼                                                              │
│   Redirect to /dashboard/                                             │
│                                                                       │
└───────────────────────────────────────────────────────────────────────┘


┌───────────────────────────────────────────────────────────────────────┐
│                     AUTHENTICATION COMPARISON                         │
├───────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  Feature          │ Web Auth              │ API Token Auth           │
│  ────────────────────────────────────────────────────────────────────│
│  Purpose          │ Browser access        │ Programmatic access      │
│  Login URL        │ /accounts/login/      │ /api/auth/login/         │
│  Auth Method      │ Session cookies       │ Token in header          │
│  Storage          │ Browser cookies       │ Client app storage       │
│  Header           │ Cookie: sessionid=... │ Authorization: Token ... │
│  Logout           │ /accounts/logout/     │ /api/auth/logout/        │
│  Persistence      │ Until browser close   │ Token doesn't expire     │
│  Use Case         │ Human users           │ Apps, scripts, mobile    │
│  Example          │ Visit /dashboard/     │ curl with -H header      │
│                                                                       │
└───────────────────────────────────────────────────────────────────────┘


┌───────────────────────────────────────────────────────────────────────┐
│                    QUICK REFERENCE                                    │
├───────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  SIGN UP:    http://localhost:8000/accounts/signup/                  │
│  LOGIN:      http://localhost:8000/accounts/login/                   │
│  DASHBOARD:  http://localhost:8000/dashboard/                        │
│  SWAGGER:    http://localhost:8000/api/docs/                         │
│  ADMIN:      http://localhost:8000/admin/                            │
│                                                                       │
│  GET TOKEN:  POST /api/auth/login/                                   │
│              {"username": "...", "password": "..."}                   │
│                                                                       │
│  USE TOKEN:  curl -H "Authorization: Token abc123..." /api/...       │
│                                                                       │
└───────────────────────────────────────────────────────────────────────┘
```

## Key Takeaways

1. **Two Independent Auth Systems**: Web (sessions) and API (tokens)
2. **Auto Customer Creation**: Django signals automatically create Customer on signup
3. **OneToOne Link**: Customer ↔ User relationship
4. **Many-to-Many**: Customer ↔ Company and Customer ↔ Item
5. **Complete REST API**: All CRUD operations with custom actions
6. **Interactive Docs**: Swagger UI for testing
7. **Clean Templates**: Custom HTML for login, signup, dashboard

## Files Created

- `api/signals.py` - Auto-create Customer on User creation
- `api/web_views.py` - Home and dashboard views
- `api/web_urls.py` - URL routing for web pages
- `templates/base.html` - Base template with navigation
- `templates/home.html` - Landing page
- `templates/dashboard.html` - User dashboard
- `templates/account/login.html` - Custom login page
- `templates/account/signup.html` - Custom signup page
- `WEB_AUTH_GUIDE.md` - Complete web auth documentation
- `SETUP_COMPLETE.md` - Full setup summary
- `QUICKSTART.md` - Quick start guide

## Status: ✅ COMPLETE AND RUNNING!
