"""
Custom forms for the console app.
"""
from django import forms
from allauth.account.forms import SignupForm
from api.models import Company


class CustomSignupForm(SignupForm):
    """
    Custom signup form that adds company selection.
    """
    company = forms.ModelChoiceField(
        queryset=Company.objects.all(),
        required=False,
        empty_label="Select a company (optional)",
        widget=forms.Select(attrs={
            'class': 'form-control',
            'id': 'id_company'
        }),
        help_text="Select the company you want to be associated with"
    )
    
    def __init__(self, *args, **kwargs):
        print("DEBUG: CustomSignupForm.__init__ called")
        super(CustomSignupForm, self).__init__(*args, **kwargs)
        # Customize field order
        field_order = ['username', 'email', 'company', 'password1', 'password2']
        self.order_fields(field_order)
        print(f"DEBUG: Form fields after init: {list(self.fields.keys())}")
    
    def custom_signup(self, request, user):
        """
        Called after the user is created but before login.
        This is the recommended way to extend signup in django-allauth.
        """
        company = self.cleaned_data.get('company')
        print(f"DEBUG: custom_signup called for user {user.username}")
        print(f"DEBUG: Company selected: {company}")
        
        if company:
            # Import here to avoid circular imports
            from api.models import Customer
            # The Customer profile should have been created by the signal
            try:
                customer = Customer.objects.get(user=user)
                customer.companies.add(company)
                customer.save()
                print(f"DEBUG: Successfully associated company {company.name} with customer {customer.user.username}")
                print(f"DEBUG: Customer companies count: {customer.companies.count()}")
            except Customer.DoesNotExist:
                # If for some reason the customer doesn't exist, 
                # we'll skip the company association
                print(f"DEBUG: ERROR - Customer profile not found for user {user.username}")
        else:
            print(f"DEBUG: No company selected for user {user.username}")
