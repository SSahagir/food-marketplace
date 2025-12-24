from rest_framework.routers import DefaultRouter
from .views import DishViewSet

router = DefaultRouter()
router.register(r'dishes', DishViewSet)
urlpatterns = router.urls