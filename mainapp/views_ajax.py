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

'''
    Production File Path :  staticfiles_storage.url(file)
    Developement File Path : settings.STATICFILES_DIRS[0] + 'app\...\.csv'
'''
book_path = settings.STATICFILES_DIRS[0] + \
            '\\mainapp\\dataset\\books.csv'

def search(request):
    '''
        AJAX request for search bar functionality
    '''
    if request.method == "POST" and request.is_ajax():
        query = request.POST.get('bookName', None)

        df_book = pd.read_csv(book_path)
        top5_result = df_book[df_book['original_title'].str.contains(
            query, regex=False, case=False)][:5]
        top5_result = json.dumps(top5_result.to_dict('records'))

        return JsonResponse({'success': True, 'top5_result': top5_result}, status=200)


def book_summary(request):
    '''
        AJAX request for book summary
    '''
    if request.method == 'POST' and request.is_ajax():
        bookid = request.POST.get('bookid', None)
        URL = 'https://www.goodreads.com/book/show/' + bookid
        page = requests.get(URL)
        soup = BeautifulSoup(page.content, 'html.parser')
        div_container = soup.find(id='description')
        booksummary = ""
        for spantag in div_container.find_all('span'):
            booksummary = spantag.text
            break
        return JsonResponse({'success': True, 'booksummary': booksummary}, status=200)


def get_book_details(request):
    '''
        AJAX request for book details
    '''
    if request.method == 'POST' and request.is_ajax():
        bookid = request.POST.get('bookid', None)
        df_book = pd.read_csv(book_path)
        book_details = df_book[df_book['book_id'] == int(bookid)]
        book_details = json.dumps(book_details.to_dict('records'))

        return JsonResponse({'success': True, 'book_details': book_details}, status=200)

