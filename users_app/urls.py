from django.urls import path
from users_app.views import profile_user, CustomLogoutView, CustomLoginView, RegisterView


app_name = "users"

urlpatterns = [
    path("login/", CustomLoginView.as_view(), name="login"),
    path("register/", RegisterView.as_view(), name="register"),
    path("logout/", CustomLogoutView.as_view(), name="logout"),
    path("profile/", profile_user, name="profile"),
]
