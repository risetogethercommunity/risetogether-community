# accounts/models.py

from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
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
    email = models.EmailField(unique=True)  # Ensure emails are unique

    USERNAME_FIELD = 'email'  # Use email for login
    REQUIRED_FIELDS = ['username'] # Still require username for createsuperuser

    # Fix reverse accessor clashes
    groups = models.ManyToManyField(
        Group,
        related_name='custom_user_groups',
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups'
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='custom_user_permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions'
    )

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"


# ------------------ PROFILE ------------------
class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile")
    profile_pic = models.ImageField(upload_to="profile_pics/", default='profile_pics/default.png', blank=True, null=True)
    bio = models.TextField(blank=True, null=True, default="Aspiring Developer | Eager to learn and collaborate with the community!")
    posts_shared_count = models.PositiveIntegerField(default=0) # We'll keep this one for now

    def __str__(self):
        return f"Profile of {self.user.username}"
    
    @property
    def blogs_count(self):
        try:
            from community.models import Blog 
            return Blog.objects.filter(author=self.user).count()
        except Exception:
            return 0

    @property
    def projects_count(self):
        try:
            from community.models import Project
            return Project.objects.filter(author=self.user).count()
        except Exception:
            return 0


class ProfileLink(models.Model):
    profile = models.ForeignKey(Profile, related_name="links", on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    url = models.URLField()

    def __str__(self):
        return f"{self.title} ({self.profile.user.username})"


# ------------------ VISITOR EXTENSIONS ------------------
class VisitorPreference(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="preferences")
    # Make sure your 'community' app has 'Blog' and 'Project' models
    # liked_posts = models.ManyToManyField("community.Blog", blank=True, related_name="liked_by")
    # liked_projects = models.ManyToManyField("community.Project", blank=True, related_name="liked_by")
    notifications_enabled = models.BooleanField(default=True)

    def __str__(self):
        return f"Preferences of {self.user.username}"


# --- Signals to create Profile and VisitorPreference on User creation ---
@receiver(post_save, sender=User)
def create_user_profile_and_preferences(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        VisitorPreference.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile_and_preferences(sender, instance, **kwargs):
    instance.profile.save()
    instance.preferences.save()