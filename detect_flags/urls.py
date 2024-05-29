
from django.urls import path

from . import views

urlpatterns = [
    path('', views.home),
    path('detect-flags/', views.detect_flags, name='detect_flags'),
]