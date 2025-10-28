from django.urls import path
from . import views

app_name = "feed"

urlpatterns = [
    # Main feed
    path("", views.feed_list, name="feed_list"),
    # Post operations
    path("post/<int:pk>/", views.post_detail, name="post_detail"),
    path("post/create/", views.create_post, name="create_post"),
    path("post/<int:pk>/edit/", views.edit_post, name="edit_post"),
    path("post/<int:pk>/delete/", views.delete_post, name="delete_post"),
    # Comment operations
    path("post/<int:post_pk>/comment/", views.add_comment, name="add_comment"),
    path("comment/<int:pk>/delete/", views.delete_comment, name="delete_comment"),
    # Like operations (AJAX)
    path("post/<int:pk>/like/", views.toggle_post_like, name="toggle_post_like"),
    path(
        "comment/<int:pk>/like/", views.toggle_comment_like, name="toggle_comment_like"
    ),
    # Save operation (AJAX)
    path("post/<int:pk>/save/", views.toggle_save_post, name="toggle_save_post"),
    # User-specific views
    path("user/<str:username>/posts/", views.user_posts, name="user_posts"),
    path("saved/", views.saved_posts, name="saved_posts"),
]
