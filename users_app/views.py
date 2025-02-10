from django.contrib import messages
from django.contrib.auth.views import LogoutView, LoginView
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.contrib import messages

from .forms import LoginForm, RegisterForm


class CustomLoginView(LoginView):
    template_name = 'login.html'
    form_class = LoginForm
    next_page = 'main'
    
    def form_valid(self, form):
        messages.success(self.request, f'Добро пожаловать, {form.get_user().username}!')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Неверное имя пользователя или пароль')
        return super().form_invalid(form)


class CustomLogoutView(LogoutView):
    template_name = 'logout.html'
    next_page = 'main'

    def post(self, request, *args, **kwargs):
        messages.success(request, 'Вы успешно вышли из системы')
        return super().post(request, *args, **kwargs)


class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = 'register.html'
    success_url = reverse_lazy('main')



def profile_user(request):
    pass
