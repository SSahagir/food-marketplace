from django.db import models
from restaurants.models import Restaurant

class Category(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self): return self.name

class Dish(models.Model):
    TYPE_CHOICES = (('veg', 'Veg'), ('non_veg', 'Non-Veg'), ('egg', 'Egg'))
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='dishes')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    image = models.ImageField(upload_to='dishes/', blank=True, null=True)
    is_available = models.BooleanField(default=True)
    food_type = models.CharField(max_length=10, choices=TYPE_CHOICES, default='veg')

    def __str__(self): return self.name