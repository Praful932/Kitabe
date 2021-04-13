from django.urls import path
from mainapp import views, views_ajax
urlpatterns = [
    path('', views.index, name='index'),
    path('genre_books/<genre>', views.genre_books, name='genre_books'),
    path('explore_books/', views.explore_books, name='explore_books'),
    path('book_recommendations/', views.book_recommendations, name='book_recommendations'),
    path('library/read_books', views.read_books, name='read_books')
]

# Ajax Views
urlpatterns += [
    path('search_ajax/', views_ajax.search, name='search_ajax'),
    path('book_summary_ajax/', views_ajax.book_summary, name='summary_ajax'),
    path('book_details_ajax/', views_ajax.get_book_details, name='book_details'),
    path('user_rate_book/', views_ajax.user_rate_book, name='user_rate_book'),
]
