from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.staticfiles.storage import staticfiles_storage
from django.contrib.auth.decorators import login_required
from mainapp.helpers import genre_wise, count_vectorizer_recommendation
from mainapp.models import UserRating
import BookRecSystem.settings as settings

from bs4 import BeautifulSoup
from math import ceil
import numpy as np
import pandas as pd
import os
import json
import requests
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
    qual = qualified[['book_id','original_title', 'authors',
                      'average_rating', 'image_url']].head(15)
    books = qual.to_dict('records')
    return render(request, 'mainapp/index.html',{ 'book':books})


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
    user_ratings = list(UserRating.objects.filter(user = request.user).order_by('-bookrating'))
    random.shuffle(user_ratings)
    best_user_ratings = sorted(user_ratings, key = operator.attrgetter('bookrating'), reverse = True)   
    if best_user_ratings:
        # If one or more book is rated
        bookid = best_user_ratings[0].bookid
        recommended_books_dict = count_vectorizer_recommendation(bookid)
    else:
        return redirect('index')
    return render(request,'mainapp/recommendation.html',{'books':recommended_books_dict})

