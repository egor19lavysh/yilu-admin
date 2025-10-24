from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages

def get_levels(request):
    return render(request, "main/levels.html")

def login_view(request):
    """Функция для аутентификации пользователей"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Аутентифицируем пользователя
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            # Если пользователь найден и парверен
            login(request, user)
            messages.success(request, f'Добро пожаловать, {user.username}!')
            return redirect('main:levels')  # Перенаправляем на страницу профиля
        else:
            # Если аутентификация не удалась
            messages.error(request, 'Неверное имя пользователя или пароль')
            return render(request, 'main/login.html', {'error': 'Invalid credentials'})
    
    # GET запрос - показываем форму логина
    return render(request, 'main/login.html')

def logout_view(request):
    """Функция для выхода из системы"""
    logout(request)
    messages.success(request, 'Вы успешно вышли из системы')
    return redirect('main:login')