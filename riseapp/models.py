from django.db import models
from tinymce.models import HTMLField
from django.utils import timezone
from accounts.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

class Contact(models.Model):
    name = models.CharField(max_length=150)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} - {self.email}"


class FAQ(models.Model):
    question = models.CharField(max_length=255)
    answer = models.TextField()

    def __str__(self):
        return self.question



class Testimonial(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="testimonials")
    name = models.CharField(max_length=150, blank=True, null=True)  # optional fallback if no user
    stars = models.PositiveSmallIntegerField(default=5)  # rating out of 5
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Testimonial ({self.stars}★)"


class SiteConfig(models.Model):
    about_us = HTMLField(blank=True, null=True)
    members_count = models.PositiveIntegerField(default=0)
    sessions_count = models.PositiveIntegerField(default=0)
    projects_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return "Site Configuration"


class Mission(models.Model):
    site_config = models.ForeignKey(SiteConfig, related_name="missions", on_delete=models.CASCADE)
    icon = models.CharField(max_length=100)  # store icon class name (like FontAwesome)
    title = models.CharField(max_length=150)
    description = models.TextField()

    def __str__(self):
        return self.title

class Achievement(models.Model):
    ICON_TYPE = (
        ('icon', 'Icon (CSS Class)'),
        ('image', 'Image (Upload)'),
    )

    title = models.CharField(max_length=255)
    awarded_by = models.CharField(max_length=255, help_text="Who gave this award/recognition")
    description = models.TextField()
    date = models.DateField()
    key_highlight = models.CharField(max_length=100, help_text="e.g. 1st Place, Winner, Award Won")
    icon_type = models.CharField(max_length=10, choices=ICON_TYPE, default='icon')
    icon_class = models.CharField(max_length=100, blank=True, null=True, help_text="CSS class e.g. fa fa-trophy")
    icon_image = models.ImageField(upload_to="achievement_icons/", blank=True, null=True)

    def __str__(self):
        return self.title