from rest_framework import serializers
from .models import Dish, Category
from django.db.models import Avg

class DishSerializer(serializers.ModelSerializer):
    rating = serializers.SerializerMethodField()
    reviews_count = serializers.SerializerMethodField()

    class Meta:
        model = Dish
        fields = '__all__'
        extra_kwargs = {
            'restaurant': {'read_only': True},  # <--- CRITICAL FIX
            'image': {'required': False}
        }

    def get_rating(self, obj):
        # Handle cases where review_set might not exist yet
        if hasattr(obj, 'review_set'):
            return obj.review_set.aggregate(Avg('rating'))['rating__avg'] or 0
        return 0

    def get_reviews_count(self, obj):
        if hasattr(obj, 'review_set'):
            return obj.review_set.count()
        return 0