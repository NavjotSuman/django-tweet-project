from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Tweet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(max_length=250)
    photo = models.ImageField(upload_to='thumbnail/', blank=True, null=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user} - {self.text[:21]}'
    
    