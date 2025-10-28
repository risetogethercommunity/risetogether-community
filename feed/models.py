from django.db import models
from django.conf import settings
from django.utils import timezone


class Post(models.Model):
    """
    Main post model - can be text, image, video, or blog reference
    """

    POST_TYPES = [
        ("text", "Text Only"),
        ("image", "Image Post"),
        ("video", "Video Post"),
        ("blog", "Blog Post"),
    ]

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="feed_posts"
    )
    post_type = models.CharField(max_length=10, choices=POST_TYPES, default="text")
    content = models.TextField(help_text="Post content/caption")

    # Media fields
    image = models.ImageField(upload_to="posts/images/", blank=True, null=True)
    video = models.FileField(upload_to="posts/videos/", blank=True, null=True)

    # Blog reference (if sharing a blog post)
    blog = models.ForeignKey(
        "community.Blog",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="shared_posts",
    )

    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_pinned = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    # Engagement tracking
    views_count = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Post"
        verbose_name_plural = "Posts"
        indexes = [
            models.Index(fields=["-created_at"]),
            models.Index(fields=["author", "-created_at"]),
        ]

    def __str__(self):
        return f"{self.author.username} - {self.post_type} - {self.created_at.strftime('%Y-%m-%d')}"

    @property
    def likes_count(self):
        return self.likes.count()

    @property
    def comments_count(self):
        return self.comments.count()

    @property
    def get_excerpt(self):
        """Return first 100 characters of content"""
        return self.content[:100] + "..." if len(self.content) > 100 else self.content


class Comment(models.Model):
    """
    Comments on posts - can be nested (replies)
    """

    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="feed_comments"
    )
    content = models.TextField()

    # For nested comments (replies)
    parent = models.ForeignKey(
        "self", on_delete=models.CASCADE, null=True, blank=True, related_name="replies"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_edited = models.BooleanField(default=False)

    class Meta:
        ordering = ["created_at"]
        verbose_name = "Comment"
        verbose_name_plural = "Comments"
        indexes = [
            models.Index(fields=["post", "created_at"]),
            models.Index(fields=["parent"]),
        ]

    def __str__(self):
        return f"Comment by {self.author.username} on {self.post.id}"

    @property
    def likes_count(self):
        return self.comment_likes.count()

    @property
    def replies_count(self):
        return self.replies.count()

    def is_reply(self):
        """Check if this comment is a reply to another comment"""
        return self.parent is not None


class PostLike(models.Model):
    """
    Likes on posts
    """

    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="likes")
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="post_likes"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("post", "user")
        verbose_name = "Post Like"
        verbose_name_plural = "Post Likes"
        indexes = [
            models.Index(fields=["post", "user"]),
        ]

    def __str__(self):
        return f"{self.user.username} likes {self.post.id}"


class CommentLike(models.Model):
    """
    Likes on comments
    """

    comment = models.ForeignKey(
        Comment, on_delete=models.CASCADE, related_name="comment_likes"
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="comment_likes"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("comment", "user")
        verbose_name = "Comment Like"
        verbose_name_plural = "Comment Likes"
        indexes = [
            models.Index(fields=["comment", "user"]),
        ]

    def __str__(self):
        return f"{self.user.username} likes comment {self.comment.id}"


class SavedPost(models.Model):
    """
    Saved/bookmarked posts by users
    """

    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="saved_by")
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="saved_posts"
    )
    saved_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("post", "user")
        verbose_name = "Saved Post"
        verbose_name_plural = "Saved Posts"
        ordering = ["-saved_at"]

    def __str__(self):
        return f"{self.user.username} saved {self.post.id}"


class HashTag(models.Model):
    """
    Hashtags for posts
    """

    name = models.CharField(max_length=100, unique=True)
    posts = models.ManyToManyField(Post, related_name="hashtag", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Hashtag"
        verbose_name_plural = "Hashtags"
        ordering = ["name"]

    @property
    def posts_count(self):
        return self.posts.count()

    def __str__(self):
        return f"#{self.name}"

    @property
    def posts_count(self):
        return self.posts.count()


class Mention(models.Model):
    """
    User mentions in posts
    """

    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="mentions")
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="mentioned_in"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("post", "user")
        verbose_name = "Mention"
        verbose_name_plural = "Mentions"

    def __str__(self):
        return f"@{self.user.username} in post {self.post.id}"
