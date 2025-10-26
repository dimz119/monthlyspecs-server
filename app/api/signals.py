"""
Signal handlers for the API app.
"""
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Customer, Role


@receiver(post_save, sender=User)
def create_customer_profile(sender, instance, created, **kwargs):
    """
    Automatically create a Customer profile when a new User is created.
    This ensures every user has an associated Customer profile with 'customer' role.
    """
    if created:
        # Get or create the 'customer' role
        customer_role, _ = Role.objects.get_or_create(
            name=Role.CUSTOMER,
            defaults={'description': 'Standard customer role'}
        )
        Customer.objects.create(user=instance, role=customer_role)


@receiver(post_save, sender=User)
def save_customer_profile(sender, instance, **kwargs):
    """
    Save the Customer profile whenever the User is saved.
    """
    try:
        instance.customer.save()
    except Customer.DoesNotExist:
        # If for some reason the customer doesn't exist, create it
        customer_role, _ = Role.objects.get_or_create(
            name=Role.CUSTOMER,
            defaults={'description': 'Standard customer role'}
        )
        Customer.objects.create(user=instance, role=customer_role)
