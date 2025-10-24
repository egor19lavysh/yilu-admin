from django.shortcuts import redirect
from django.urls import reverse
from django.conf import settings
from django.shortcuts import render
import re

class AdvancedAuthMiddleware:
    """
    Продвинутый middleware с гибкой настройкой прав доступа
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # URL, доступные без аутентификации
        PUBLIC_URLS = [
            '/login/',
            '/logout/',
            '/admin/login/'
        ]


        # Проверяем, является ли URL публичным
        is_public_url = any(
            request.path.startswith(url) or 
            re.match(url, request.path) for url in PUBLIC_URLS
        )

        # Если URL не публичный и пользователь не авторизован
        if not is_public_url and not request.user.is_authenticated:
            return redirect('main:login')

        # Если пользователь авторизован
        if request.user.is_authenticated:
            # Проверяем доступ для не-staff пользователей
            if not request.user.is_staff:
                return render(request, "main/access_denied.html")

        return self.get_response(request)