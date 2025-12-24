from django.contrib import admin
from .models import Restaurant

@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'whatsapp_number')
    search_fields = ('name',)