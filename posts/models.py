from django.db import models
from django.contrib.auth.models import User

class Blog(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    cover_image = models.ImageField(upload_to='blogs/', blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField(User, related_name="liked_blogs", blank=True)
    stars = models.ManyToManyField(User, related_name="starred_blogs", blank=True)
    bookmarks = models.ManyToManyField(User, related_name="bookmarked_blogs", blank=True)

    class Meta:
        ordering = ['-created_at']

    @property
    def read_time(self):
     wpm = 200
     word_count = len(self.content.split())
     return max(1, round(word_count / 50))

    def __str__(self):
        return self.title