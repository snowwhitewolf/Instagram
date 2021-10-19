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

# class FeedComment(models.Model):
#     comment = models.TextField()


# class FeedImage(models.Model):
#     feed = models.ForeignKey(Feed, on_delete=models.CASCADE)
#     image = models.ImageField(default='media/diary/default_image.jpeg', upload_to='media/',
#                               blank=True, null=True)
#     def __str__(self):
#         return self.title
