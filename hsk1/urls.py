from django.urls import path
from hsk1 import views

app_name = "hsk1"

urlpatterns = [
    path('', views.ListeningListView.as_view(), name='listening_list'),
    path('<int:pk>/', views.ListeningDetailView.as_view(), name='listening_detail'),
    path('create/', views.ListeningCreateView.as_view(), name='listening_create'),
    path('<int:pk>/update/', views.ListeningUpdateView.as_view(), name='listening_update'),
    path('<int:pk>/delete/', views.ListeningDeleteView.as_view(), name='listening_delete'),
]
