from django.urls import path
from . import views


app_name = "hsk4"

urlpatterns = [
    path("", views.get_sections, name="sections"),
    path('listening/', views.ListeningListView.as_view(), name='listening_list'),
    path('listening/<int:pk>/', views.ListeningDetailView.as_view(), name='listening_detail'),
    path('listening/create/', views.ListeningCreateView.as_view(), name='listening_create'),
    path('listening/<int:pk>/update/', views.ListeningUpdateView.as_view(), name='listening_update'),
    path('listening/<int:pk>/delete/', views.ListeningDeleteView.as_view(), name='listening_delete'),
    path('reading/', views.ReadingListView.as_view(), name='reading_list'),
    path('reading/<int:pk>/', views.ReadingDetailView.as_view(), name='reading_detail'),
    path('reading/create/', views.ReadingCreateView.as_view(), name='reading_create'),
    path('reading/<int:pk>/update/', views.ReadingUpdateView.as_view(), name='reading_update'),
    path('reading/<int:pk>/delete/', views.ReadingDeleteView.as_view(), name='reading_delete'),
    path('writing/', views.WritingListView.as_view(), name='writing_list'),
    path('writing/<int:pk>/', views.WritingDetailView.as_view(), name='writing_detail'),
    path('writing/create/', views.WritingCreateView.as_view(), name='writing_create'),
    path('writing/<int:pk>/update/', views.WritingUpdateView.as_view(), name='writing_update'),
    path('writing/<int:pk>/delete/', views.WritingDeleteView.as_view(), name='writing_delete'),
]
