from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name= 'home'),
    path('rankings/', views.rankings, name='top500'),
    path('about/', views.about, name= 'about'),
]