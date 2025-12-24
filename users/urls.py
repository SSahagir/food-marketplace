from django.urls import path
from .views import login_view, register_with_otp, request_otp, verify_reset_password, profile_view, get_notifications

urlpatterns = [
    path('login/', login_view),
    path('request-otp/', request_otp),
    path('register-verify/', register_with_otp),
    path('reset-password/', verify_reset_password),
    path('profile/', profile_view),
    path('notifications/', get_notifications),
]