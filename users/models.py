from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = (
        ('customer', 'Customer'),
        ('restaurant', 'Restaurant'),
        ('delivery', 'Delivery Partner'),
    )
    email = models.EmailField(unique=True)  # Enforce unique email
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='customer')
    phone = models.CharField(max_length=15, blank=True, null=True)
    date_of_birth = models.DateField(null=True, blank=False) # Mandatory DOB

    REQUIRED_FIELDS = ['email', 'first_name', 'last_name', 'date_of_birth']

class Notification(models.Model):
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    message = models.CharField(max_length=255)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta: ordering = ['-created_at']

class OTP(models.Model):
    email = models.EmailField()
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now=True)