from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q
from .models import Order, OrderMessage
from .serializers import OrderSerializer, OrderMessageSerializer
from users.models import Notification

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get_queryset(self):
        user = self.request.user
        if not user.is_authenticated: return Order.objects.none()
        
        if user.role == 'restaurant':
            return Order.objects.filter(dishes__restaurant__owner=user).distinct().order_by('-created_at')
        elif user.role == 'delivery':
            # See orders available for pickup OR assigned to this driver
            return Order.objects.filter(
                Q(status='ready_for_pickup', delivery_partner=None) | 
                Q(delivery_partner=user)
            ).distinct().order_by('-created_at')
        
        # Customer
        return Order.objects.filter(customer=user).order_by('-created_at')

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        
        # Notify Restaurant
        order = serializer.instance
        first_dish = order.dishes.first()
        if first_dish:
            rest_owner = first_dish.restaurant.owner
            Notification.objects.create(recipient=rest_owner, message=f"New Order #{order.id} for ${order.total_price}")
            
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @action(detail=True, methods=['get'])
    def messages(self, request, pk=None):
        order = self.get_object()
        msgs = order.messages.all().order_by('created_at')
        return Response(OrderMessageSerializer(msgs, many=True).data)

    @action(detail=True, methods=['post'])
    def send_message(self, request, pk=None):
        order = self.get_object()
        OrderMessage.objects.create(order=order, sender=request.user, text=request.data['text'])
        return Response({'status': 'sent'})

    @action(detail=True, methods=['patch'])
    def update_status(self, request, pk=None):
        order = self.get_object()
        new_status = request.data.get('status')
        user = request.user
        
        # LOGIC MATRIX
        if user.role == 'restaurant':
            if new_status == 'confirmed': new_status = 'preparing'
            # Restaurant marks ready, system waits for driver
            if new_status == 'ready_for_pickup': pass 
            elif new_status == 'cancelled' and order.status != 'ordered':
                return Response({'error': 'Too late to cancel'}, status=400)
                
        elif user.role == 'delivery':
            # Driver accepts job
            if new_status == 'accepted':
                if order.status != 'ready_for_pickup': return Response({'error': 'Order not ready'}, 400)
                if order.delivery_partner: return Response({'error': 'Already taken'}, 400)
                order.delivery_partner = user
                new_status = 'out_for_delivery'
            
            elif new_status == 'delivered':
                if order.delivery_partner != user: return Response({'error': 'Not your order'}, 403)
        
        else:
            return Response({'error': 'Unauthorized'}, status=403)

        order.status = new_status
        order.save()
        
        # Notify Customer
        Notification.objects.create(recipient=order.customer, message=f"Order #{order.id}: {new_status.replace('_', ' ')}")
        
        return Response({'status': 'updated', 'current_status': order.status})