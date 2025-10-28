from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Create a router and register viewsets
router = DefaultRouter()
router.register(r'roles', views.RoleViewSet, basename='role')
router.register(r'companies', views.CompanyViewSet, basename='company')
router.register(r'customers', views.CustomerViewSet, basename='customer')
router.register(r'items', views.ItemViewSet, basename='item')
router.register(r'users', views.UserViewSet, basename='user')
router.register(r'purchase-history', views.PurchaseHistoryViewSet, basename='purchase-history')

urlpatterns = [
    # Auth endpoints
    path('auth/login/', views.login_view, name='login'),
    path('auth/logout/', views.logout_view, name='logout'),
    
    # API endpoints
    path('', include(router.urls)),
]
