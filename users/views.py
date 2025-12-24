from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.core.mail import send_mail
from django.conf import settings
from django.db.models import Sum
import random

from .serializers import UserSerializer, NotificationSerializer
from .models import User, Notification, OTP
from restaurants.models import Restaurant
from orders.models import Order

def generate_otp(): return str(random.randint(100000, 999999))
def send_otp_email(email, code):
    try:
        send_mail("FoodMarket Verification", f"Code: {code}", settings.EMAIL_HOST_USER, [email], fail_silently=False)
        return True
    except: return False

@api_view(['POST'])
@permission_classes([AllowAny])
def request_otp(request):
    email, purpose = request.data.get('email'), request.data.get('purpose')
    if not email: return Response({'error': 'Email required'}, 400)
    if purpose == 'register' and User.objects.filter(email=email).exists(): return Response({'error': 'Email exists'}, 400)
    if purpose == 'reset' and not User.objects.filter(email=email).exists(): return Response({'error': 'Email not found'}, 404)
    code = generate_otp()
    OTP.objects.update_or_create(email=email, defaults={'code': code})
    print(f"OTP for {email}: {code}") # Console fallback
    send_otp_email(email, code)
    return Response({'message': 'OTP Sent'})

@api_view(['POST'])
@permission_classes([AllowAny])
def verify_reset_password(request):
    email, code, pwd = request.data.get('email'), request.data.get('otp'), request.data.get('new_password')
    try:
        OTP.objects.get(email=email, code=code).delete()
        u = User.objects.get(email=email)
        u.set_password(pwd)
        u.save()
        return Response({'message': 'Password reset'})
    except: return Response({'error': 'Invalid OTP'}, 400)

@api_view(['POST'])
@permission_classes([AllowAny])
@parser_classes([MultiPartParser, FormParser, JSONParser])
def register_with_otp(request):
    d = request.data
    try:
        OTP.objects.get(email=d.get('email'), code=d.get('otp')).delete()
        u = User.objects.create_user(username=d.get('username'), email=d.get('email'), password=d.get('password'), first_name=d.get('first_name'), last_name=d.get('last_name'), date_of_birth=d.get('date_of_birth'), role=d.get('role'))
        if u.role == 'restaurant':
            Restaurant.objects.create(owner=u, name=d.get('restaurant_name'), address=d.get('address'), image=request.FILES.get('image'))
        return Response({'refresh': str(RefreshToken.for_user(u)), 'access': str(RefreshToken.for_user(u).access_token), 'user': UserSerializer(u).data})
    except Exception as e: return Response({'error': str(e)}, 400)

@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    u = authenticate(username=request.data.get('username'), password=request.data.get('password'))
    if u: return Response({'refresh': str(RefreshToken.for_user(u)), 'access': str(RefreshToken.for_user(u).access_token), 'user': UserSerializer(u).data})
    return Response({'error': 'Invalid Credentials'}, 400)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_notifications(request):
    return Response(NotificationSerializer(Notification.objects.filter(recipient=request.user)[:20], many=True).data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def profile_view(request):
    tid = request.query_params.get('user_id')
    u = User.objects.get(id=tid) if tid and str(tid)!=str(request.user.id) else request.user
    me = (u == request.user)
    resp = {'user': UserSerializer(u).data, 'role': u.role, 'details': {}, 'stats': {}}
    
    if u.role == 'restaurant':
        try:
            r = Restaurant.objects.get(owner=u)
            resp['details'] = {'id': r.id, 'name': r.name, 'address': r.address, 'image': r.image.url if r.image else None}
            if me: resp['stats'] = {'revenue': Order.objects.filter(dishes__restaurant=r).aggregate(Sum('total_price'))['total_price__sum'] or 0}
        except: pass
    elif u.role == 'delivery' and me:
        ords = Order.objects.filter(delivery_partner=u)
        resp['stats'] = {'deliveries': ords.filter(status='delivered').count(), 'earnings': ords.filter(status='delivered').count()*5}
    else:
        resp['stats'] = {'orders': Order.objects.filter(customer=u).count()}
    return Response(resp)