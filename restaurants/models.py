from django.db import models
from users.models import User

class Restaurant(models.Model):
    owner = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    address = models.TextField()
    image = models.ImageField(upload_to='restaurants/', blank=True, null=True)
    whatsapp_number = models.CharField(max_length=15)
    
    def __str__(self):
        return self.name