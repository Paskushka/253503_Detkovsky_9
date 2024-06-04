from django.urls import path
from . import views

urlpatterns = [
    path('', views.myzei_home, name='myzei_home')
]