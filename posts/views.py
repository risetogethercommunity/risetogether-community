from django.shortcuts import render, redirect
from .models import Post
from .forms import PostForm
from django.views.generic.edit import UpdateView, DeleteView
from django.urls import reverse_lazy 

def post_list(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("post_list")
    else:
        form = PostForm()

    posts = Post.objects.all().order_by("-created_at")
    return render(request, "posts/posts.html", {"form": form, "posts": posts})
 # Update Post
class PostUpdateView(UpdateView):
    model = Post
    form_class = PostForm  
    template_name = "posts/post_edit.html"
    success_url = reverse_lazy("post_list")  # redirect after update

# Delete Post
class PostDeleteView(DeleteView):
    model = Post
    template_name = "posts/post_confirm_delete.html"
    success_url = reverse_lazy("post_list")  # redirect after delete
