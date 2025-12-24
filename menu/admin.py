from django.contrib import admin
from .models import Category, Dish

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Dish)
class DishAdmin(admin.ModelAdmin):
    list_display = ('name', 'restaurant', 'price', 'category', 'is_available')
    list_filter = ('restaurant', 'category', 'is_available')
    search_fields = ('name',)