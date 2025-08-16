from django.urls import path
from . import views
from .views import PostUpdateView, PostDeleteView

urlpatterns = [
    path("", views.post_list, name="post_list"),
    path('post/<int:pk>/edit/', PostUpdateView.as_view(), name="post_edit"),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name="post_delete"),
]
