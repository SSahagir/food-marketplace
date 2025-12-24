from django.db import models
from users.models import User
from menu.models import Dish

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE, related_name='review_set')
    rating = models.IntegerField()  # 1-10
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)