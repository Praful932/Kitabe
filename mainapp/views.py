from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.staticfiles.storage import staticfiles_storage
import BookRecSystem.settings as settings

from bs4 import BeautifulSoup
import pandas as pd
import os
import json
import requests
 
                               #----------------------------------------------- Home page -----------------------------------------------------------------------#

def index(request):
    return render(request, 'mainapp/index.html')


                                 #----------------------------------------------- Search book -----------------------------------------------------------------------#
 
def search_ajax(request):
    if request.method == "POST" and request.is_ajax():
        query = request.POST.get('bookName', None)        

        # Production File path
        # staticfiles_storage.url(file)

        # Development File path
        book_path = settings.STATICFILES_DIRS[0] + '\\mainapp\\dataset\\books.csv'

        df_book = pd.read_csv(book_path)
        top5_result = df_book[df_book['original_title'].str.contains(query, regex=False, case = False)][:5]
        top5_result = json.dumps(top5_result.to_dict('records'))
        
        return JsonResponse({'success' : True, 'top5_result' : top5_result}, status = 200)

                           #----------------------------------------------- Book Summary  -----------------------------------------------------------------------#

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



                   #----------------------------------------------- Genre -----------------------------------------------------------------------#

def art(request):
    top_genre = genre_wise("art")
    genre_topbooks = top_genre.to_dict('records')
    genre_name = ({'Art'})
    return render(request,'mainapp/genre.html',{'genre':genre_name,'genre_topbook': genre_topbooks})

def biography(request):
    top_genre = genre_wise("biography")
    genre_topbooks = top_genre.to_dict('records')
    genre_name = ({'Biography'})
    return render(request,'mainapp/genre.html',{'genre':genre_name,'genre_topbook': genre_topbooks})
 
def business(request):
    top_genre = genre_wise("business")
    genre_topbooks = top_genre.to_dict('records')
    genre_name = ({'Business'})
    return render(request,'mainapp/genre.html',{'genre':genre_name,'genre_topbook': genre_topbooks})

def chicklit(request):
    top_genre = genre_wise("Chick Lit")
    genre_topbooks = top_genre.to_dict('records')
    genre_name = ({'Chick Lit'})
    return render(request,'mainapp/genre.html',{'genre':genre_name,'genre_topbook': genre_topbooks})    

def children(request):
    top_genre = genre_wise("Children's")
    genre_topbooks = top_genre.to_dict('records')
    genre_name = ({"Children's"})
    return render(request,'mainapp/genre.html',{'genre':genre_name,'genre_topbook': genre_topbooks})    

def christian(request):
    top_genre = genre_wise("Christian")
    genre_topbooks = top_genre.to_dict('records')
    genre_name = ({'Christian'})
    return render(request,'mainapp/genre.html',{'genre':genre_name,'genre_topbook': genre_topbooks})    

def comics(request):
    top_genre = genre_wise("Comics")
    genre_topbooks = top_genre.to_dict('records')
    genre_name = ({'Comics'})
    return render(request,'mainapp/genre.html',{'genre':genre_name,'genre_topbook': genre_topbooks}) 

def contemporary(request):
    top_genre = genre_wise("Contemporary")
    genre_topbooks = top_genre.to_dict('records')
    genre_name = ({'Contemporary'})
    return render(request,'mainapp/genre.html',{'genre':genre_name,'genre_topbook': genre_topbooks}) 

def classics(request):
    top_genre = genre_wise("Classics")
    genre_topbooks = top_genre.to_dict('records')
    genre_name = ({'Classics'})
    return render(request,'mainapp/genre.html',{'genre':genre_name,'genre_topbook': genre_topbooks})    

def cookbooks(request):
    top_genre = genre_wise("Cookbooks")
    genre_topbooks = top_genre.to_dict('records')
    genre_name = ({'Cookbooks'})
    return render(request,'mainapp/genre.html',{'genre':genre_name,'genre_topbook': genre_topbooks}) 

def crime(request):
    top_genre = genre_wise("Crime")
    genre_topbooks = top_genre.to_dict('records')
    genre_name = ({'Crime'})
    return render(request,'mainapp/genre.html',{'genre':genre_name,'genre_topbook': genre_topbooks}) 

def ebooks(request):
    top_genre = genre_wise("Ebooks")
    genre_topbooks = top_genre.to_dict('records')
    genre_name = ({'Ebooks'})
    return render(request,'mainapp/genre.html',{'genre':genre_name,'genre_topbook': genre_topbooks}) 

def fantasy(request):
    top_genre = genre_wise("Fantasy")
    genre_topbooks = top_genre.to_dict('records')
    genre_name = ({'Fantasy'})
    return render(request,'mainapp/genre.html',{'genre':genre_name,'genre_topbook': genre_topbooks}) 

def fiction(request):
    top_genre = genre_wise("Fiction")
    genre_topbooks = top_genre.to_dict('records')
    genre_name = ({'Fiction'})
    return render(request,'mainapp/genre.html',{'genre':genre_name,'genre_topbook': genre_topbooks}) 

def gayandlesbian(request):
    top_genre = genre_wise("Gay and Lesbian")
    genre_topbooks = top_genre.to_dict('records')
    genre_name = ({'Gay and Lesbian'})
    return render(request,'mainapp/genre.html',{'genre':genre_name,'genre_topbook': genre_topbooks}) 

def graphicnovels(request):
    top_genre = genre_wise("Graphic Novels")
    genre_topbooks = top_genre.to_dict('records')
    genre_name = ({'Graphic Novels'})
    return render(request,'mainapp/genre.html',{'genre':genre_name,'genre_topbook': genre_topbooks})     


def historicalfiction(request):
    top_genre = genre_wise("Historical Fiction")
    genre_topbooks = top_genre.to_dict('records')
    genre_name = ({'Historical Fiction'})
    return render(request,'mainapp/genre.html',{'genre':genre_name,'genre_topbook': genre_topbooks}) 

def history(request):
    top_genre = genre_wise("History")
    genre_topbooks = top_genre.to_dict('records')
    genre_name = ({'History'})
    return render(request,'mainapp/genre.html',{'genre':genre_name,'genre_topbook': genre_topbooks}) 

def horror(request):
    top_genre = genre_wise("Horror")
    genre_topbooks = top_genre.to_dict('records')
    genre_name = ({'Horror'})
    return render(request,'mainapp/genre.html',{'genre':genre_name,'genre_topbook': genre_topbooks})   

def humorandcomedy(request):
    top_genre = genre_wise("Humor and Comedy")
    genre_topbooks = top_genre.to_dict('records')
    genre_name = ({'Humor and Comedy'})
    return render(request,'mainapp/genre.html',{'genre':genre_name,'genre_topbook': genre_topbooks})   

def manga(request):
    top_genre = genre_wise("Manga")
    genre_topbooks = top_genre.to_dict('records')
    genre_name = ({'Manga'})
    return render(request,'mainapp/genre.html',{'genre':genre_name,'genre_topbook': genre_topbooks})     

def memoir(request):
    top_genre = genre_wise("Memoir")
    genre_topbooks = top_genre.to_dict('records')
    genre_name = ({'Memoir'})
    return render(request,'mainapp/genre.html',{'genre':genre_name,'genre_topbook': genre_topbooks})   

def music(request):
    top_genre = genre_wise("Music")
    genre_topbooks = top_genre.to_dict('records')
    genre_name = ({'Music'})
    return render(request,'mainapp/genre.html',{'genre':genre_name,'genre_topbook': genre_topbooks})     

def mystery(request):
    top_genre = genre_wise("Mystery")
    genre_topbooks = top_genre.to_dict('records')
    genre_name = ({'Mystery'})
    return render(request,'mainapp/genre.html',{'genre':genre_name,'genre_topbook': genre_topbooks})       

def nonfiction(request):
    top_genre = genre_wise("Nonfiction")
    genre_topbooks = top_genre.to_dict('records')
    genre_name = ({'Nonfiction'})
    return render(request,'mainapp/genre.html',{'genre':genre_name,'genre_topbook': genre_topbooks}) 

def paranormal(request):
    top_genre = genre_wise("Paranormal")
    genre_topbooks = top_genre.to_dict('records')
    genre_name = ({'Paranormal'})
    return render(request,'mainapp/genre.html',{'genre':genre_name,'genre_topbook': genre_topbooks}) 

def philosophy(request):
    top_genre = genre_wise("Philosophy")
    genre_topbooks = top_genre.to_dict('records')
    genre_name = ({'Philosophy'})
    return render(request,'mainapp/genre.html',{'genre':genre_name,'genre_topbook': genre_topbooks}) 

def poetry(request):
    top_genre = genre_wise("Poetry")
    genre_topbooks = top_genre.to_dict('records')
    genre_name = ({'Poetry'})
    return render(request,'mainapp/genre.html',{'genre':genre_name,'genre_topbook': genre_topbooks}) 

def psychology(request):
    top_genre = genre_wise("Psychology")
    genre_topbooks = top_genre.to_dict('records')
    genre_name = ({'Psychology'})
    return render(request,'mainapp/genre.html',{'genre':genre_name,'genre_topbook': genre_topbooks}) 

def religion(request):
    top_genre = genre_wise("Religion")
    genre_topbooks = top_genre.to_dict('records')
    genre_name = ({'Religion'})
    return render(request,'mainapp/genre.html',{'genre':genre_name,'genre_topbook': genre_topbooks})     

def romance(request):
    top_genre = genre_wise("Romance")
    genre_topbooks = top_genre.to_dict('records')
    genre_name = ({'Romance'})
    return render(request,'mainapp/genre.html',{'genre':genre_name,'genre_topbook': genre_topbooks})   

def science(request):
    top_genre = genre_wise("Science")
    genre_topbooks = top_genre.to_dict('records')
    genre_name = ({'Science'})
    return render(request,'mainapp/genre.html',{'genre':genre_name,'genre_topbook': genre_topbooks})       

def sciencefiction(request):
    top_genre = genre_wise("Science Fiction")
    genre_topbooks = top_genre.to_dict('records')
    genre_name = ({'Science Fiction'})
    return render(request,'mainapp/genre.html',{'genre':genre_name,'genre_topbook': genre_topbooks})  

def selfhelp(request):
    top_genre = genre_wise("Self Help")
    genre_topbooks = top_genre.to_dict('records')
    genre_name = ({'Self Help'})
    return render(request,'mainapp/genre.html',{'genre':genre_name,'genre_topbook': genre_topbooks})      

def suspense(request):
    top_genre = genre_wise("Suspense")
    genre_topbooks = top_genre.to_dict('records')
    genre_name = ({'Suspense'})
    return render(request,'mainapp/genre.html',{'genre':genre_name,'genre_topbook': genre_topbooks})      

def spirituality(request):
    top_genre = genre_wise("Spirituality")
    genre_topbooks = top_genre.to_dict('records')
    genre_name = ({'Spirituality'})
    return render(request,'mainapp/genre.html',{'genre':genre_name,'genre_topbook': genre_topbooks})  

def sports(request):
    top_genre = genre_wise("Sports")
    genre_topbooks = top_genre.to_dict('records')
    genre_name = ({'Sports'})
    return render(request,'mainapp/genre.html',{'genre':genre_name,'genre_topbook': genre_topbooks})  

def thriller(request):
    top_genre = genre_wise("Thriller")
    genre_topbooks = top_genre.to_dict('records')
    genre_name = ({'Thriller'})
    return render(request,'mainapp/genre.html',{'genre':genre_name,'genre_topbook': genre_topbooks})      

def travel(request):
    top_genre = genre_wise("Travel")
    genre_topbooks = top_genre.to_dict('records')
    genre_name = ({'Travel'})
    return render(request,'mainapp/genre.html',{'genre':genre_name,'genre_topbook': genre_topbooks})      

def youngadult(request):
    top_genre = genre_wise("Young Adult")
    genre_topbooks = top_genre.to_dict('records')
    genre_name = ({'Young Adult'})
    return render(request,'mainapp/genre.html',{'genre':genre_name,'genre_topbook': genre_topbooks})   

def genre_wise(genre,percentile=0.85):
    df_books = pd.read_csv("static/mainapp/dataset/books.csv")
    available_genres_books = pd.read_csv("static/mainapp/dataset/genre.csv")
    df = available_genres_books[available_genres_books['genre'] == genre.lower()]
    qualified = pd.merge(df_books,df,left_on='book_id', right_on = 'book_id', how ='inner')
    v = qualified['ratings_count']
    m = qualified['ratings_count'].quantile(percentile)
    R = qualified['average_rating']
    C = qualified['average_rating'].mean()
    qualified['weighted_rating'] = (R*v + C*m) / (v + m)
    qualified.sort_values('weighted_rating', ascending=False, inplace=True)
    cols = ['original_title','authors','average_rating','image_url']
    return qualified[cols].head(15)
    