from rest_framework import serializers
from .models import Order, OrderMessage

class OrderMessageSerializer(serializers.ModelSerializer):
    sender_name = serializers.SerializerMethodField()
    class Meta:
        model = OrderMessage
        fields = ['id', 'sender', 'sender_name', 'text', 'created_at']
    def get_sender_name(self, obj): return obj.sender.username

class OrderSerializer(serializers.ModelSerializer):
    restaurant_name = serializers.SerializerMethodField()
    customer_name = serializers.SerializerMethodField() # Added
    
    class Meta:
        model = Order
        fields = '__all__'
        
    def get_restaurant_name(self, obj):
        first_dish = obj.dishes.first()
        return first_dish.restaurant.name if first_dish else "Unknown"

    def get_customer_name(self, obj):
        return obj.customer.username