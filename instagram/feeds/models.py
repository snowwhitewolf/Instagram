from django.db import models

# Create your models here.
class Feed(models.Model):
    # title = models.CharField(max_length=100)
    content = models.TextField()
    image = models.ImageField(upload_to='media/', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    location = models.TextField(blank=True)
    like = models.IntegerField(blank=True)

    def __str__(self):
        return self.title

