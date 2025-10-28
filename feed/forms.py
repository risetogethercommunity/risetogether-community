from django import forms
from .models import Post, Comment


class PostForm(forms.ModelForm):
    """Form for creating and editing posts"""

    class Meta:
        model = Post
        fields = ["post_type", "content", "image", "video", "blog"]
        widgets = {
            "post_type": forms.Select(attrs={"class": "form-select", "id": "postType"}),
            "content": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                    "placeholder": "What's on your mind?",
                    "id": "postContent",
                }
            ),
            "image": forms.FileInput(
                attrs={
                    "class": "form-control",
                    "accept": "image/*",
                    "id": "postImage",
                    "style": "display: block; width: 100%;",
                }
            ),
            "video": forms.FileInput(
                attrs={
                    "class": "form-control",
                    "accept": "video/*",
                    "id": "postVideo",
                    "style": "display: block; width: 100%;",
                }
            ),
            "blog": forms.Select(attrs={"class": "form-select", "id": "postBlog"}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

        # Make fields optional by default
        self.fields["image"].required = False
        self.fields["video"].required = False
        self.fields["blog"].required = False

        # Filter blogs to only show user's own blogs
        if self.user:
            from community.models import Blog

            self.fields["blog"].queryset = Blog.objects.filter(author=self.user)

    def clean(self):
        cleaned_data = super().clean()
        post_type = cleaned_data.get("post_type")
        content = cleaned_data.get("content")
        image = cleaned_data.get("image")
        video = cleaned_data.get("video")
        blog = cleaned_data.get("blog")

        # Validation: Ensure content or media is provided
        if post_type == "text" and not content:
            raise forms.ValidationError("Text posts must have content.")

        if post_type == "image" and not image:
            raise forms.ValidationError("Image posts must have an image.")

        if post_type == "video" and not video:
            raise forms.ValidationError("Video posts must have a video.")

        if post_type == "blog" and not blog:
            raise forms.ValidationError("Blog posts must be linked to a blog.")

        return cleaned_data


class CommentForm(forms.ModelForm):
    """Form for adding comments to posts"""

    class Meta:
        model = Comment
        fields = ["content"]
        widgets = {
            "content": forms.Textarea(
                attrs={
                    "class": "form-control comment-input",
                    "rows": 2,
                    "placeholder": "Write a comment...",
                    "id": "commentContent",
                }
            ),
        }

    def clean_content(self):
        content = self.cleaned_data.get("content")
        if not content or not content.strip():
            raise forms.ValidationError("Comment cannot be empty.")
        return content.strip()


class ReplyForm(forms.ModelForm):
    """Form for replying to comments"""

    class Meta:
        model = Comment
        fields = ["content"]
        widgets = {
            "content": forms.Textarea(
                attrs={
                    "class": "form-control reply-input",
                    "rows": 2,
                    "placeholder": "Write a reply...",
                }
            ),
        }

    def clean_content(self):
        content = self.cleaned_data.get("content")
        if not content or not content.strip():
            raise forms.ValidationError("Reply cannot be empty.")
        return content.strip()
