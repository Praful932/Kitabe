from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from mainapp.helpers import genre_wise, count_vectorizer_recommendations, get_book_dict, svd_recommendations, get_rated_bookids, combine_ids
from mainapp.models import UserRating

import pandas as pd
import random
import operator


def index(request):
    '''
        Homepage
    '''
    df_books = pd.read_csv("static/mainapp/dataset/books.csv")
    df_books1 = df_books
    v = df_books1['ratings_count']
    m = df_books1['ratings_count'].quantile(0.95)
    R = df_books1['average_rating']
    C = df_books1['average_rating'].mean()
    W = (R*v + C*m) / (v + m)
    df_books['weighted_rating'] = W
    qualified = df_books1.sort_values(
        'weighted_rating', ascending=False).head(250)
    qual = qualified[['book_id', 'original_title', 'authors',
                      'average_rating', 'image_url']].head(15)
    books = qual.to_dict('records')
    return render(request, 'mainapp/index.html', {'book': books})


def genre_books(request, genre):
    '''
        View to render Books in a particular genre
    '''
    top_genre = genre_wise(genre)
    genre_topbooks = top_genre.to_dict('records')
    context = {
        'genre': genre.capitalize(),
        'genre_topbook': genre_topbooks,
    }
    return render(request, 'mainapp/genre.html', context)


@login_required
def book_recommendations(request):
    '''
        View to render book recommendations

        Count Vectorizer Approach:
            1. Get Ratings of User
            2. Shuffle by Top Ratings(For Randomness each time)
            3. Recommend according to Top Rated Book
    '''
    user_ratings = list(UserRating.objects.filter(user=request.user).order_by('-bookrating'))
    random.shuffle(user_ratings)
    best_user_ratings = sorted(user_ratings, key=operator.attrgetter('bookrating'), reverse=True)
    if best_user_ratings:
        # If one or more book is rated
        bookid = best_user_ratings[0].bookid

        already_rated_books = set(get_rated_bookids(user_ratings))

        # Get bookids based on Count Vectorizer
        cv_bookids = set(count_vectorizer_recommendations(bookid))
        # Get Top 10 bookids based on svd
        svd_bookids = set(svd_recommendations(user_ratings))

        best_bookids = combine_ids(cv_bookids, svd_bookids, already_rated_books)
        all_books_dict = get_book_dict(best_bookids)
    else:
        return redirect('index')
    return render(request, 'mainapp/recommendation.html', {'books': all_books_dict})
