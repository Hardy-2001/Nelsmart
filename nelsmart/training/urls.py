from django.urls import path
from . import views

urlpatterns = [
    path('apply/', views.apply_training, name='apply_training'),
]