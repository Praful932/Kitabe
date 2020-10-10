import pandas as pd
import numpy as np
import os
import BookRecSystem.settings as settings

book_path = os.path.join(settings.STATICFILES_DIRS[0] + '/mainapp/dataset/books.csv')
cosin_sim_path = os.path.join(settings.STATICFILES_DIRS[0] + '/mainapp/model_files/cosine_rating_sim.npz')
book_indices_path = os.path.join(settings.STATICFILES_DIRS[0] + '/mainapp/model_files/indices.pkl')
cols = ['original_title', 'authors', 'average_rating', 'image_url', 'book_id']


def genre_wise(genre, percentile=0.85):
    df_books = pd.read_csv("static/mainapp/dataset/books.csv")
    available_genres_books = pd.read_csv("static/mainapp/dataset/genre.csv")
    df = available_genres_books[available_genres_books['genre'] == genre.lower()]
    qualified = pd.merge(df_books, df, left_on='book_id', right_on ='book_id', how ='inner')
    v = qualified['ratings_count']
    m = qualified['ratings_count'].quantile(percentile)
    R = qualified['average_rating']
    C = qualified['average_rating'].mean()
    qualified['weighted_rating'] = (R*v + C*m) / (v + m)
    qualified.sort_values('weighted_rating', ascending=False, inplace=True)
    return qualified[cols].head(15)
    

def count_vectorizer_recommendation(bookid):
    '''
        Returns recommened book ids based on book details
    '''
    df_book = pd.read_csv(book_path)
    indices = pd.read_pickle(book_indices_path)
    cosine_sim = np.load(cosin_sim_path)['array1']

    book_title = df_book[df_book['book_id'] == int(bookid)]['original_title'].values[0]
    book_title = book_title.replace(' ','').lower()
    idx = indices[book_title]

    # Get this books sim with all other books, enum to keep track of book index
    sim_scores = list(enumerate(cosine_sim[idx]))   
    sim_scores = sorted(sim_scores, key =lambda x: x[1], reverse =True)
    sim_scores = sim_scores[1:10]

    book_indices =  [i[0] for i in sim_scores]
    rec_books_dict = df_book.loc[book_indices, cols].to_dict('records')

    return rec_books_dict


