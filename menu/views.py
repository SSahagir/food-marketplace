from rest_framework import viewsets, permissions, serializers, status, filters
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from django_filters.rest_framework import DjangoFilterBackend
from .models import Dish
from .serializers import DishSerializer
from restaurants.models import Restaurant

class IsDishOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS: return True
        return obj.restaurant.owner == request.user

class DishViewSet(viewsets.ModelViewSet):
    queryset = Dish.objects.all()
    serializer_class = DishSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsDishOwnerOrReadOnly]
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    
    # Enable Search and Filtering
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['name', 'description', 'category__name', 'restaurant__name']
    filterset_fields = ['food_type', 'restaurant']
    
    def perform_create(self, serializer):
        user = self.request.user
        if user.role == 'restaurant':
            try:
                restaurant = Restaurant.objects.get(owner=user)
                serializer.save(restaurant=restaurant)
            except Restaurant.DoesNotExist:
                raise serializers.ValidationError("Restaurant profile missing.")
        else:
            raise serializers.PermissionDenied("Only restaurants can create dishes.")