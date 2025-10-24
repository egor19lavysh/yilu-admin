from django.urls import path
from . import views


app_name = "main"

urlpatterns = [
    path("", views.get_levels, name="levels"),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]
