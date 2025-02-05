from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth.views import LogoutView, LoginView

from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy

from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.urls import reverse
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


def register_user(request):
    """View функция для регистрации пользователя"""
    
    # Если пользователь уже авторизован - редиректим на главную
    if request.user.is_authenticated:
        return redirect('main')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        
        # Проверяем совпадение паролей
        if password1 != password2:
            messages.error(request, 'Пароли не совпадают')
            return render(request, 'register.html')
        
        # Проверяем существование пользователя
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Пользователь с таким именем уже существует')
            return render(request, 'register.html')
        
        # Проверяем существование email
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Пользователь с таким email уже существует')
            return render(request, 'register.html')
        
        # Создаем пользователя
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password1
        )
        
        # Авторизуем пользователя
        login(request, user)
        messages.success(request, f'Добро пожаловать, {user.username}!')
        return redirect('main')
        
    return render(request, 'register.html')



def profile_user(request):
    pass
