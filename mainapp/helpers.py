import pandas as pd

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
    cols = ['original_title','authors','average_rating','image_url','book_id']
    return qualified[cols].head(15)
    