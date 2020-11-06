from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from mainapp.helpers import genre_wise, count_vectorizer_recommendations, get_book_dict, get_rated_bookids, combine_ids, embedding_recommendations, get_books, top_books_this_week
from mainapp.models import UserRating
from django.contrib import messages

import random
import operator


def index(request):
    '''
        View to render Homepage
    '''
    books = top_books_this_week().to_dict('records')
    return render(request, 'mainapp/index.html', {'books': books})


def genre_books(request, genre):
    '''
        View to render Books in a particular genre
    '''
    genre_topbooks = genre_wise(genre)
    genre_topbooks = genre_topbooks.to_dict('records')
    context = {
        'genre': genre.capitalize(),
        'genre_topbook': genre_topbooks,
    }
    return render(request, 'mainapp/genre.html', context)


def explore_books(request):
    '''
        View to Render Explore Page
    '''
    sample = get_books()
    return render(request, 'mainapp/explore.html', {'book': sample})


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

    if len(best_user_ratings) < 4:
        messages.info(request, 'Please rate atleast 5 books')
        return redirect('index')
    if best_user_ratings:
        # If one or more book is rated
        bookid = best_user_ratings[0].bookid
        already_rated_books = set(get_rated_bookids(user_ratings))
        # Get bookids based on Count Vectorizer
        cv_bookids = set(count_vectorizer_recommendations(bookid))

        # Shuffle again for randomness for second approach
        random.shuffle(user_ratings)
        best_user_ratings = sorted(user_ratings, key=operator.attrgetter('bookrating'), reverse=True)
        # Get Top 10 bookids based on embedding
        embedding_bookids = set(embedding_recommendations(best_user_ratings))

        best_bookids = combine_ids(cv_bookids, embedding_bookids, already_rated_books)
        all_books_dict = get_book_dict(best_bookids)
    else:
        return redirect('index')
    return render(request, 'mainapp/recommendation.html', {'books': all_books_dict})
