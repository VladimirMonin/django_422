from django.urls import path
from users_app.views import CustomLogoutView, CustomLoginView, RegisterView, ProfileDetailView, ProfileEditView, ProfilePasswordView


app_name = "users"

urlpatterns = [
    path("login/", CustomLoginView.as_view(), name="login"),
    path("register/", RegisterView.as_view(), name="register"),
    path("logout/", CustomLogoutView.as_view(), name="logout"),
    path("profile/<int:pk>/", ProfileDetailView.as_view(), name="profile_detail"),
    path("profile/<int:pk>/edit/", ProfileEditView.as_view(), name="profile_edit"),
    path("profile/<int:pk>/password/", ProfilePasswordView.as_view(), name="profile_password"),
]