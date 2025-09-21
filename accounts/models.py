from django.db import models
from django.contrib.auth.models import AbstractUser
from tinymce.models import HTMLField


# ------------------ USER ------------------
class User(AbstractUser):
    ROLE_CHOICES = (
        ('community_lead', 'Community Lead'),
        ('deputy_lead', 'Deputy Lead'),
        ('co_lead', 'Co-Lead'),
        ('member', 'General Member'),
        ('visitor', 'Visitor'),
    )

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='visitor')

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"


# ------------------ PROFILE ------------------
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    profile_pic = models.ImageField(upload_to="profile_pics/", blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    activity_score = models.PositiveIntegerField(default=0)
    leaderboard_rank = models.PositiveIntegerField(default=0)
    posts_shared_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"Profile of {self.user.username}"


class ProfileLink(models.Model):
    profile = models.ForeignKey(Profile, related_name="links", on_delete=models.CASCADE)
    title = models.CharField(max_length=100)   # e.g., GitHub, LinkedIn
    url = models.URLField()

    def __str__(self):
        return f"{self.title} ({self.profile.user.username})"


# ------------------ VISITOR EXTENSIONS ------------------
class VisitorPreference(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="preferences")
    liked_posts = models.ManyToManyField("Blog", blank=True, related_name="liked_by")
    liked_projects = models.ManyToManyField("Project", blank=True, related_name="liked_by")
    # we will create Comment model later and link it here
    notifications_enabled = models.BooleanField(default=True)

    def __str__(self):
        return f"Preferences of {self.user.username}"
