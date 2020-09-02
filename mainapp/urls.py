from django.urls import path
from mainapp.views import index
urlpatterns = [
    path('', index),
]