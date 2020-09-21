from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.staticfiles.storage import staticfiles_storage
from mainapp.helpers import genre_wise
import BookRecSystem.settings as settings

from bs4 import BeautifulSoup
from math import ceil
import pandas as pd
import os
import json
import requests


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
    qual = qualified[['original_title', 'authors',
                      'average_rating', 'weighted_rating', 'image_url']].head(15)
    books = qual.to_dict('records')
    n = len(df_books1)
    nSlides = n//4 + ceil((n/4)-(n//4))
    params = {'no_of_slides': nSlides,
              'range': range(1, nSlides), 'book': books}
    return render(request, 'mainapp/index.html', params)


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

