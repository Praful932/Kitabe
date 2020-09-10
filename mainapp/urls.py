from django.urls import path
from mainapp import views
urlpatterns = [
    path('', views.index, name='index'),
    path('search_ajax/', views.search_ajax, name='search_ajax'),
    path('book_summary_ajax/', views.book_summary_ajax, name='summary_ajax'),
]