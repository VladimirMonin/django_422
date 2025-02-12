"""
View - базовая вью - можно определить методы get, post - и там определить логику обработки запросов
ListView - списковое отображение
DetailView - детальное отображение одного объекта
CreateView - создание объекта (указываем, форму и шаблон)
UpdateView - обновление объекта (указываем, форму и шаблон)
DeleteView - удаление объекта (указываем, форму и шаблон)
TemplateView - базовый класс для шаблонов
"""

from django.contrib import messages
from django.contrib.auth.views import LogoutView, LoginView, PasswordChangeView
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic import TemplateView
from django.urls import reverse_lazy
from django.contrib import messages

from .forms import LoginForm, RegisterForm, CustomPasswordChangeForm, ProfileEditForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView
from django.contrib.auth import get_user_model


class OwnerPermissionMixin:
    """
    Миксин для проверки прав доступа к профилю
    """

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["is_owner"] = self.request.user == self.get_object()
        return context


class CustomLoginView(LoginView):
    template_name = "login.html"
    form_class = LoginForm
    next_page = "main"

    def form_valid(self, form):
        messages.success(self.request, f"Добро пожаловать, {form.get_user().username}!")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Неверное имя пользователя или пароль")
        return super().form_invalid(form)


class CustomLogoutView(LogoutView):
    template_name = "logout.html"
    next_page = "main"

    def post(self, request, *args, **kwargs):
        messages.success(request, "Вы успешно вышли из системы")
        return super().post(request, *args, **kwargs)


class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = "register.html"
    success_url = reverse_lazy("main")


class ProfileDetailView(LoginRequiredMixin, OwnerPermissionMixin, DetailView):
    model = get_user_model()
    template_name = "profile_detail.html"
    context_object_name = "profile_user"



class ProfilePasswordView(LoginRequiredMixin, PasswordChangeView):
    template_name = "profile_password.html"
    form_class = CustomPasswordChangeForm
    # Реверс с аргументом pk

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["profile_user"] = self.request.user
        return context

    def get_success_url(self):
        return reverse_lazy("users:profile_detail", kwargs={"pk": self.request.user.pk})


class ProfileEditView(LoginRequiredMixin, UpdateView):
    form_class = ProfileEditForm
    template_name = "profile_edit.html"

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return reverse_lazy("users:profile_detail", kwargs={"pk": self.request.user.pk})

    def form_valid(self, form):
        messages.success(self.request, "Профиль успешно обновлен")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["profile_user"] = self.request.user
        return context
