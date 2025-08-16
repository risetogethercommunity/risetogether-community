from django.db import models

# Create your models here.

class Post(models.Model):
    CONTENT_TYPE_CHOICES = [
        ('image', 'Image'),
        ('video', 'Video'),
        ('code', 'Code'),
    ]

    content = models.TextField()  # Text content of the post
    attachment_type = models.CharField(max_length=10, choices=CONTENT_TYPE_CHOICES, blank=True, null=True)
    image = models.ImageField(upload_to="posts/images/", blank=True, null=True)
    video = models.FileField(upload_to="posts/videos/", blank=True, null=True)
    code = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Post {self.id} - {self.content[:30]}"
