from django.urls import path
from users_app.views import register_user, profile_user, CustomLogoutView, CustomLoginView


app_name = "users"

urlpatterns = [
    path("login/", CustomLoginView.as_view(), name="login"),
    path("register/", register_user, name="register"),
    path("logout/", CustomLogoutView.as_view(), name="logout"),
    path("profile/", profile_user, name="profile"),
]
