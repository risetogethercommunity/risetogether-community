from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.db.models import Q, Count, Prefetch
from .models import Post, Comment, PostLike, CommentLike, SavedPost, HashTag, Mention
from .forms import PostForm, CommentForm, ReplyForm
from accounts.models import Profile
from django.contrib.auth import get_user_model

User = get_user_model()


@login_required
def feed_list(request):
    """Display the main feed with all posts"""

    # Get all active posts, ordered by creation date
    posts = (
        Post.objects.filter(is_active=True)
        .select_related("author", "author__profile")
        .prefetch_related("likes", "comments__author", "hashtag", "mentions__user")
        .annotate(
            total_likes=Count("likes", distinct=True),
            total_comments=Count("comments", distinct=True),
        )
        .order_by("-is_pinned", "-created_at")
    )

    # Filter by hashtag if provided
    hashtag = request.GET.get("hashtag")
    if hashtag:
        posts = posts.filter(hashtag__name=hashtag)

    # Get user's liked posts for UI state
    user_liked_posts = set(
        PostLike.objects.filter(user=request.user).values_list("post_id", flat=True)
    )

    # Get user's saved posts
    user_saved_posts = set(
        SavedPost.objects.filter(user=request.user).values_list("post_id", flat=True)
    )

    context = {
        "posts": posts,
        "user_liked_posts": user_liked_posts,
        "user_saved_posts": user_saved_posts,
        "post_form": PostForm(user=request.user),
        "comment_form": CommentForm(),
        "active_hashtag": hashtag,
    }

    return render(request, "feed/feed_list.html", context)


@login_required
def post_detail(request, pk):
    """Display a single post with all its comments"""

    post = get_object_or_404(
        Post.objects.select_related("author", "author__profile"), pk=pk, is_active=True
    )

    # Increment view count
    post.views_count += 1
    post.save(update_fields=["views_count"])

    # Get all comments (including replies)
    comments = (
        post.comments.select_related("author", "author__profile", "parent")
        .prefetch_related("comment_likes")
        .order_by("created_at")
    )

    # Organize comments into parent-child structure
    comment_dict = {}
    top_level_comments = []

    for comment in comments:
        comment_dict[comment.id] = comment
        comment.replies_list = []

        if comment.parent_id is None:
            top_level_comments.append(comment)

    for comment in comments:
        if comment.parent_id:
            parent = comment_dict.get(comment.parent_id)
            if parent:
                parent.replies_list.append(comment)

    # Check if user liked the post
    user_liked = PostLike.objects.filter(post=post, user=request.user).exists()

    # Check if user saved the post
    user_saved = SavedPost.objects.filter(post=post, user=request.user).exists()

    # Get user's liked comments
    user_liked_comments = set(
        CommentLike.objects.filter(user=request.user, comment__post=post).values_list(
            "comment_id", flat=True
        )
    )

    context = {
        "post": post,
        "comments": top_level_comments,
        "comment_form": CommentForm(),
        "reply_form": ReplyForm(),
        "user_liked": user_liked,
        "user_saved": user_saved,
        "user_liked_comments": user_liked_comments,
    }

    return render(request, "feed/post_detail.html", context)


@login_required
@require_POST
def create_post(request):
    """Create a new post"""

    form = PostForm(request.POST, request.FILES, user=request.user)

    if form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.save()

        # Process hashtags from content
        import re

        hashtags = re.findall(r"#(\w+)", post.content)
        for tag in hashtags:
            hashtag_obj, created = HashTag.objects.get_or_create(name=tag.lower())
            post.hashtag.add(hashtag_obj)

        # Process mentions from content
        mentions = re.findall(r"@(\w+)", post.content)
        for username in mentions:
            try:
                mentioned_user = User.objects.get(username=username)
                Mention.objects.create(post=post, user=mentioned_user)
            except User.DoesNotExist:
                pass

        messages.success(request, "Post created successfully!")
        return redirect("feed:feed_list")

    else:
        for error in form.errors.values():
            messages.error(request, error)
        return redirect("feed:feed_list")


@login_required
@require_POST
def add_comment(request, post_pk):
    """Add a comment to a post"""

    post = get_object_or_404(Post, pk=post_pk, is_active=True)
    form = CommentForm(request.POST)

    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.author = request.user

        # Check if this is a reply to another comment
        parent_id = request.POST.get("parent_id")
        if parent_id:
            parent_comment = get_object_or_404(Comment, pk=parent_id)
            comment.parent = parent_comment

        comment.save()

        messages.success(request, "Comment added successfully!")

    else:
        messages.error(request, "Failed to add comment.")

    return redirect("feed:post_detail", pk=post_pk)


@login_required
@require_POST
def toggle_post_like(request, pk):
    """Toggle like on a post (AJAX endpoint)"""

    post = get_object_or_404(Post, pk=pk, is_active=True)

    like, created = PostLike.objects.get_or_create(post=post, user=request.user)

    if not created:
        # Unlike
        like.delete()
        liked = False
    else:
        # Like
        liked = True

    # Return JSON response
    return JsonResponse({"liked": liked, "likes_count": post.likes.count()})


@login_required
@require_POST
def toggle_comment_like(request, pk):
    """Toggle like on a comment (AJAX endpoint)"""

    comment = get_object_or_404(Comment, pk=pk)

    like, created = CommentLike.objects.get_or_create(
        comment=comment, user=request.user
    )

    if not created:
        # Unlike
        like.delete()
        liked = False
    else:
        # Like
        liked = True

    # Return JSON response
    return JsonResponse({"liked": liked, "likes_count": comment.comment_likes.count()})


@login_required
@require_POST
def toggle_save_post(request, pk):
    """Toggle save/bookmark a post (AJAX endpoint)"""

    post = get_object_or_404(Post, pk=pk, is_active=True)

    saved, created = SavedPost.objects.get_or_create(post=post, user=request.user)

    if not created:
        # Unsave
        saved.delete()
        is_saved = False
    else:
        # Save
        is_saved = True

    # Return JSON response
    return JsonResponse({"saved": is_saved})


@login_required
def delete_post(request, pk):
    """Delete a post (only by author)"""

    post = get_object_or_404(Post, pk=pk, author=request.user)
    post.delete()

    messages.success(request, "Post deleted successfully!")
    return redirect("feed:feed_list")


@login_required
def edit_post(request, pk):
    """Edit a post (only by author)"""

    post = get_object_or_404(Post, pk=pk, author=request.user)

    if request.method == "POST":
        form = PostForm(request.POST, request.FILES, instance=post, user=request.user)

        if form.is_valid():
            form.save()
            messages.success(request, "Post updated successfully!")
            return redirect("feed:post_detail", pk=pk)

    else:
        form = PostForm(instance=post, user=request.user)

    context = {
        "form": form,
        "post": post,
        "is_edit": True,
    }

    return render(request, "feed/edit_post.html", context)


@login_required
def delete_comment(request, pk):
    """Delete a comment (only by author)"""

    comment = get_object_or_404(Comment, pk=pk, author=request.user)
    post_pk = comment.post.pk
    comment.delete()

    messages.success(request, "Comment deleted successfully!")
    return redirect("feed:post_detail", pk=post_pk)


@login_required
def user_posts(request, username):
    """Display all posts by a specific user"""

    user = get_object_or_404(User, username=username)

    posts = (
        Post.objects.filter(author=user, is_active=True)
        .select_related("author", "author__profile")
        .prefetch_related("likes", "comments")
        .order_by("-created_at")
    )

    # Get user's liked posts
    user_liked_posts = set(
        PostLike.objects.filter(user=request.user).values_list("post_id", flat=True)
    )

    # Get user's saved posts
    user_saved_posts = set(
        SavedPost.objects.filter(user=request.user).values_list("post_id", flat=True)
    )

    context = {
        "profile_user": user,
        "posts": posts,
        "user_liked_posts": user_liked_posts,
        "user_saved_posts": user_saved_posts,
        "comment_form": CommentForm(),
    }

    return render(request, "feed/user_posts.html", context)


@login_required
def saved_posts(request):
    """Display all posts saved by the current user"""

    saved_post_ids = SavedPost.objects.filter(user=request.user).values_list(
        "post_id", flat=True
    )

    posts = (
        Post.objects.filter(id__in=saved_post_ids, is_active=True)
        .select_related("author", "author__profile")
        .prefetch_related("likes", "comments")
        .order_by("-created_at")
    )

    # Get user's liked posts
    user_liked_posts = set(
        PostLike.objects.filter(user=request.user).values_list("post_id", flat=True)
    )

    context = {
        "posts": posts,
        "user_liked_posts": user_liked_posts,
        "user_saved_posts": set(saved_post_ids),
        "comment_form": CommentForm(),
        "is_saved_view": True,
    }

    return render(request, "feed/saved_posts.html", context)
