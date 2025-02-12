from django.urls import path
from users_app.views import CustomLogoutView, CustomLoginView, RegisterView, ProfileDetailView, ProfileEditView, ProfilePasswordView
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView
from .forms import CustomPasswordResetForm

app_name = "users"

urlpatterns = [
    path("login/", CustomLoginView.as_view(), name="login"),
    path("register/", RegisterView.as_view(), name="register"),
    path("logout/", CustomLogoutView.as_view(), name="logout"),
    path("profile/<int:pk>/", ProfileDetailView.as_view(), name="profile_detail"),
    path("profile/<int:pk>/edit/", ProfileEditView.as_view(), name="profile_edit"),
    path("profile/<int:pk>/password/", ProfilePasswordView.as_view(), name="profile_password"),

    # Восстановление пароля
     path('password-reset/', 
         PasswordResetView.as_view(
             template_name='password_reset.html',
             form_class=CustomPasswordResetForm,
             success_url='/users/password-reset/done/',
             template_name='password_reset.html'
         ),
         name='password_reset'),

         path('password-reset/done/', 
         PasswordResetDoneView.as_view(
             template_name='password_reset_done.html'
         ),
         name='password_reset_done'),
]