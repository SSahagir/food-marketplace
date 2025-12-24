from django.db import models
from users.models import User
from menu.models import Dish

class Order(models.Model):
    STATUS_CHOICES = (
        ('ordered', 'Ordered'),
        ('preparing', 'Preparing'),
        ('ready_for_pickup', 'Ready for Pickup'), # New status
        ('out_for_delivery', 'Out for Delivery'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    )
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    delivery_partner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='deliveries') # New field
    dishes = models.ManyToManyField(Dish)
    total_price = models.DecimalField(max_digits=8, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ordered')
    delivery_location = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

class OrderMessage(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)