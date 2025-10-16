from django.urls import path
from . import views


app_name = "main"

urlpatterns = [
    path("", views.get_levels, name="levels")
]
