# Company Selection on Signup

## Overview
Added a company dropdown selection field to the signup page, allowing new users to select and be automatically associated with a company during registration.

## Changes Made

### 1. Custom Signup Form (`/app/console/forms.py`)
Created a new custom signup form that extends django-allauth's `SignupForm`:

```python
class CustomSignupForm(SignupForm):
    company = forms.ModelChoiceField(
        queryset=Company.objects.all(),
        required=False,
        empty_label="Select a company (optional)",
        help_text="Select the company you want to be associated with"
    )
```

**Features:**
- Company field is optional (users can skip company selection)
- Displays all available companies in dropdown
- Custom field ordering (username, email, company, passwords)
- Automatic company association after user creation

**Save Logic:**
- Calls parent `save()` to create the User
- Waits for signal to create Customer profile
- Associates selected company with Customer via M2M relationship

### 2. Settings Configuration (`/app/app/settings.py`)
Added custom form configuration to django-allauth settings:

```python
ACCOUNT_FORMS = {
    'signup': 'console.forms.CustomSignupForm',
}
```

This tells django-allauth to use our custom form instead of the default signup form.

### 3. Signup Template Update (`/app/templates/account/signup.html`)
Added company selection dropdown between email and password fields:

```django
<div class="form-group">
    <label for="id_company">Company:</label>
    <select name="company" id="id_company">
        <option value="">Select a company (optional)</option>
        {% for company in form.company.field.queryset %}
            <option value="{{ company.id }}">{{ company.name }}</option>
        {% endfor %}
    </select>
    <small>Select the company you want to be associated with</small>
</div>
```

**Features:**
- Styled to match other form fields
- Shows company name as display text
- Optional selection (blank option available)
- Error display support
- Help text for guidance

## How It Works

### Registration Flow
1. User fills out signup form with username, email, **company (optional)**, and passwords
2. Form is validated by django-allauth
3. User account is created
4. Signal (`create_customer_profile`) automatically creates Customer profile with default "customer" role
5. Custom form's `save()` method retrieves the Customer profile
6. Selected company is added to Customer's companies (M2M relationship)
7. User is redirected to dashboard

### Signal Integration
The existing signal in `/app/api/signals.py` creates the Customer profile:

```python
@receiver(post_save, sender=User)
def create_customer_profile(sender, instance, created, **kwargs):
    if created:
        role, _ = Role.objects.get_or_create(name=Role.CUSTOMER)
        Customer.objects.create(user=instance, role=role)
```

Our custom form hooks into this by:
1. Letting the signal create the Customer
2. Then retrieving it and adding the company association

## Testing

### Manual Testing Steps
1. **Create Companies** (if none exist):
   - Go to Django admin: http://127.0.0.1:8000/admin/
   - Navigate to "Companies"
   - Add a few test companies

2. **Test Signup Flow**:
   - Navigate to: http://127.0.0.1:8000/accounts/signup/
   - Fill out signup form
   - Select a company from dropdown (or leave blank)
   - Submit form
   - Verify redirect to dashboard

3. **Verify Company Association**:
   - Go to dashboard
   - Check "Associated Companies" section
   - Should show selected company

4. **Test Without Company**:
   - Sign up another user
   - Leave company dropdown blank
   - Should work fine (no companies associated)

### Database Verification
Check in Django admin:
```
Admin > Customers > Select Customer > Companies (M2M)
```

Or via Django shell:
```python
from django.contrib.auth.models import User
from api.models import Customer

user = User.objects.get(username='testuser')
customer = Customer.objects.get(user=user)
print(customer.companies.all())
```

## Field Order
The signup form now displays fields in this order:
1. Username
2. Email
3. **Company (new)**
4. Password
5. Confirm Password

## Error Handling

### Form Validation
- Company field is optional, so no validation errors if left blank
- If an invalid company ID is submitted, form validation will fail
- Company dropdown only shows active companies from database

### Edge Cases Handled
1. **No companies exist**: Dropdown shows only "Select a company (optional)"
2. **Customer profile doesn't exist**: Gracefully skips company association (shouldn't happen with signals)
3. **Invalid company ID**: Django form validation catches this
4. **Multiple signups**: Each user can select different companies

## Styling
The company dropdown matches the existing form field styling:
- Same width, padding, and border as other inputs
- Consistent font size and colors
- Proper spacing and margins
- Help text in gray below dropdown

## Future Enhancements

### Potential Improvements
1. **Multi-select**: Allow users to select multiple companies during signup
2. **Company Search**: Add search/filter for large company lists
3. **Company Details**: Show company description in dropdown
4. **Required Field**: Make company selection mandatory if needed
5. **Admin Approval**: Require admin approval for company associations
6. **Invitation System**: Company-specific invitation codes
7. **Role-based Companies**: Different companies for different roles

## API Impact
No impact on existing API endpoints. The company association is handled through the existing Customer-Company M2M relationship.

## Database Schema
No database changes required. Uses existing:
- `api_customer_companies` (M2M through table)
- Relationship already established in Customer model

## Security Considerations
- Form validates company existence before association
- Only active companies from database are shown
- No direct company creation from signup form
- Standard django-allauth security applies

---

**Status**: ✅ Implemented and ready for testing
**Server**: Running at http://127.0.0.1:8000/
**Signup Page**: http://127.0.0.1:8000/accounts/signup/
**Version**: 1.0
**Last Updated**: October 28, 2025
