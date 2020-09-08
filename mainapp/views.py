from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.staticfiles.storage import staticfiles_storage
import BookRecSystem.settings as settings

from bs4 import BeautifulSoup
import pandas as pd
import os
import json
import requests

def index(request):
    return render(request, 'mainapp/index.html')

def search_ajax(request):
    if request.method == "POST" and request.is_ajax():
        query = request.POST.get('bookName', None)        

        # Production File path
        # staticfiles_storage.url(file)

        # Development File path
        book_path = settings.STATICFILES_DIRS[0] + '\\mainapp\\csv\\db.csv'

        df_book = pd.read_csv(book_path)
        top5_result = df_book[df_book['original_title'].str.contains(query, regex=False, case = False)][:5]
        top5_result = json.dumps(top5_result.to_dict('records'))
        
        return JsonResponse({'success' : True, 'top5_result' : top5_result}, status = 200)

def book_summary_ajax(request):
    if request.method == 'POST' and request.is_ajax():
        bookid = request.POST.get('bookid', None)
        URL = 'https://www.goodreads.com/book/show/' + bookid
        page = requests.get(URL)
        soup = BeautifulSoup(page.content, 'html.parser')
        div_container = soup.find(id = 'description')
        booksummary = ""
        for spantag in div_container.find_all('span'):
            booksummary = spantag.text
            break
        return JsonResponse({'success' : True, 'booksummary' : booksummary}, status = 200)
    
