from django.urls import path
from . import views

# rest
urlpatterns = [
    path('', views.api, name='api'),
    path('api-list/', views.api_list, name='api-list'),
    path('api-create/', views.api_create, name='api-create'),
    path('api-read/<int:pk>/', views.api_read, name='api-read'),
    path('api-update/<int:pk>/', views.api_update, name='api-update'),
    path('api-delete/<int:pk>/', views.api_delete, name='api-delete'),
]

