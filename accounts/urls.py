from django.urls import path
from . import views

app_name = "accounts"  # <-- add this line

urlpatterns = [
    path("join/", views.join_view, name="join"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("profile/", views.profile_view, name="profile"),
]
