from django.urls import path
from . import views

urlpatterns = [
    path('health/', views.health_check, name='health-check'),
    path('hide/', views.hide_secret, name='hide-secret'),
    path('reveal/<str:key>/', views.reveal_secret, name='reveal-secret'),
    path('redis-info/', views.get_redis_info, name='redis-info'),
]