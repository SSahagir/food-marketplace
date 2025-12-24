from django.contrib import admin
from .models import Order

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'restaurant_name', 'total_price', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    
    def restaurant_name(self, obj):
        # Helper to show restaurant name even though it's a ManyToMany relationship via dishes
        # We'll just grab the restaurant from the first dish
        first_dish = obj.dishes.first()
        if first_dish:
            return first_dish.restaurant.name
        return "N/A"