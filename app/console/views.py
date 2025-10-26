"""
Web views for rendering HTML pages (not API endpoints).
"""
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from api.models import Customer


def home(request):
    """
    Home/landing page - shows before login.
    """
    return render(request, 'home.html')


@login_required
def dashboard(request):
    """
    Dashboard page - shows after login.
    Displays customer information if a Customer profile exists.
    """
    try:
        customer = Customer.objects.get(user=request.user)
    except Customer.DoesNotExist:
        customer = None
    
    context = {
        'user': request.user,
        'customer': customer,
    }
    return render(request, 'dashboard.html', context)
