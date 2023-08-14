from django.urls import path
from . import views

urlpatterns = [
    path('play/', views.gameHome, name='play'),
    path('play/result/', views.calculateElO, name='result'),
    path('rankings/top500', views.top500, name='top500'),
]