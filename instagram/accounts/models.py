from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

# Create your models here.
class User(AbstractUser):
    # email = models.EmailField()
    profile_image = models.ImageField(upload_to='media/', blank=True)