from django.urls import path
from users_app.views import login_user, register_user, logout_user, profile_user


app_name = "users"

urlpatterns = [
    path("login/", login_user, name="login"),
    path("register/", register_user, name="register"),
    path("logout/", logout_user, name="logout"),
    path("profile/", profile_user, name="profile"),
]
