from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['content', 'attachment_type', 'image', 'video', 'code']

    def clean(self):
        cleaned_data = super().clean()
        attachment_type = cleaned_data.get("attachment_type")

        # Enforce only one type of attachment
        if attachment_type == "image" and not cleaned_data.get("image"):
            self.add_error("image", "Please upload an image.")
        elif attachment_type == "video" and not cleaned_data.get("video"):
            self.add_error("video", "Please upload a video.")
        elif attachment_type == "code" and not cleaned_data.get("code"):
            self.add_error("code", "Please enter code.")

        return cleaned_data
