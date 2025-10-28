"""
Web views for rendering HTML pages (not API endpoints).
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from api.models import Customer, Company, PurchaseHistory


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
        customer = Customer.objects.select_related('role').get(user=request.user)
    except Customer.DoesNotExist:
        customer = None
    
    context = {
        'user': request.user,
        'customer': customer,
        'show_sidebar': True,  # Enable sidebar for dashboard
    }
    return render(request, 'dashboard.html', context)


@login_required
def customer_list(request):
    """
    Customer list page - shows customers belonging to the same company.
    Only accessible to owners and managers.
    """
    try:
        customer = Customer.objects.select_related('role').prefetch_related('companies').get(user=request.user)
    except Customer.DoesNotExist:
        messages.error(request, 'Customer profile not found.')
        return redirect('dashboard')
    
    # Check if user has owner or manager role
    if not customer.role or customer.role.name not in ['owner', 'manager']:
        messages.error(request, 'You do not have permission to view customers.')
        return redirect('dashboard')
    
    # Get all companies the current user belongs to
    user_companies = customer.companies.all()
    
    # Get all customers who belong to the same companies
    customers = Customer.objects.filter(
        companies__in=user_companies
    ).select_related('user', 'role').prefetch_related('companies').distinct().order_by('user__username')
    
    context = {
        'user': request.user,
        'customer': customer,
        'customers': customers,
        'user_companies': user_companies,
        'show_sidebar': True,
    }
    return render(request, 'customers.html', context)


@login_required
def company_list(request):
    """
    Company list page - shows companies the user belongs to.
    """
    try:
        customer = Customer.objects.select_related('role').prefetch_related('companies').get(user=request.user)
    except Customer.DoesNotExist:
        messages.error(request, '고객 프로필을 찾을 수 없습니다.')
        return redirect('dashboard')
    
    # Get all companies the current user belongs to
    companies = customer.companies.all().order_by('name')
    
    context = {
        'user': request.user,
        'customer': customer,
        'companies': companies,
        'show_sidebar': True,
    }
    return render(request, 'companies.html', context)


@login_required
def company_detail(request, company_id):
    """
    Company detail/edit page - shows and allows editing company information.
    Only users who belong to the company can view/edit it.
    Only owners and managers can edit.
    """
    try:
        customer = Customer.objects.select_related('role').prefetch_related('companies').get(user=request.user)
    except Customer.DoesNotExist:
        messages.error(request, '고객 프로필을 찾을 수 없습니다.')
        return redirect('dashboard')
    
    # Get the company and verify user has access to it
    company = get_object_or_404(Company, id=company_id)
    
    if company not in customer.companies.all():
        messages.error(request, '이 회사 정보에 접근할 권한이 없습니다.')
        return redirect('company_list')
    
    # Check if user can edit (only owner and manager)
    can_edit = customer.role and customer.role.name in ['owner', 'manager']
    
    if request.method == 'POST' and can_edit:
        # Update company information
        company.name = request.POST.get('name', company.name)
        company.description = request.POST.get('description', company.description)
        company.address = request.POST.get('address', company.address)
        company.phone = request.POST.get('phone', company.phone)
        company.email = request.POST.get('email', company.email)
        company.website = request.POST.get('website', company.website)
        
        try:
            company.save()
            messages.success(request, f'{company.name} 정보가 성공적으로 업데이트되었습니다.')
            return redirect('company_detail', company_id=company.id)
        except Exception as e:
            messages.error(request, f'업데이트 중 오류가 발생했습니다: {str(e)}')
    
    # Get customer count for this company
    customer_count = customer.companies.filter(id=company_id).first().customers.count() if company else 0
    
    context = {
        'user': request.user,
        'customer': customer,
        'company': company,
        'can_edit': can_edit,
        'customer_count': customer_count,
        'show_sidebar': True,
    }
    return render(request, 'company_detail.html', context)


@login_required
def purchase_list(request):
    """
    Purchase history page - shows purchase history for the logged-in customer.
    Only accessible to customers.
    """
    try:
        customer = Customer.objects.select_related('role').get(user=request.user)
    except Customer.DoesNotExist:
        messages.error(request, '고객 프로필을 찾을 수 없습니다.')
        return redirect('dashboard')
    
    # Get all purchase history for this customer
    purchases = PurchaseHistory.objects.filter(
        customer=customer
    ).select_related('item').order_by('-purchase_date')
    
    # Calculate statistics
    total_purchases = purchases.count()
    total_spent = sum(p.total_price for p in purchases)
    average_purchase = total_spent / total_purchases if total_purchases > 0 else 0
    
    context = {
        'user': request.user,
        'customer': customer,
        'purchases': purchases,
        'total_purchases': total_purchases,
        'total_spent': total_spent,
        'average_purchase': average_purchase,
        'show_sidebar': True,
    }
    return render(request, 'purchases.html', context)
