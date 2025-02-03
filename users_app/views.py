from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.urls import reverse


from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.urls import reverse


def login_user(request):
    """View функция для авторизации пользователя"""

    # Если пользователь уже авторизован - редиректим на главную
    if request.user.is_authenticated:
        return redirect("main")

    # Если POST запрос - обрабатываем форму
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        # Пытаемся авторизовать пользователя
        user = authenticate(request, username=username, password=password)

        # Если пользователь найден
        if user is not None:
            # Авторизуем пользователя
            login(request, user)
            messages.success(request, f"Добро пожаловать, {user.username}!")
            return redirect("main")
        else:
            # Если пользователь не найден - показываем ошибку
            messages.error(request, "Неверное имя пользователя или пароль")

    return render(request, "login.html")


def logout_user(request):
    """View функция для выхода пользователя из системы"""

    # Если пользователь не авторизован - редиректим на главную
    if not request.user.is_authenticated:
        return redirect("main")

    # Если POST запрос - выходим из системы
    if request.method == "POST":
        logout(request)
        messages.success(request, "Вы успешно вышли из системы")
        return redirect("main")

    return render(request, "logout.html")


def register_user(request):
    pass


def profile_user(request):
    pass
