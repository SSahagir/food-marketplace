from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

# Register custom user model
admin.site.register(User, UserAdmin)