import pandas as pd
import numpy as np
import os
from scipy.spatial.distance import cdist
import BookRecSystem.settings as settings

# For Count Vectorizer
book_path = os.path.join(settings.STATICFILES_DIRS[0] + '/mainapp/dataset/books.csv')
cosin_sim_path = os.path.join(settings.STATICFILES_DIRS[0] + '/mainapp/model_files/cosine_rating_sim.npz')
book_indices_path = os.path.join(settings.STATICFILES_DIRS[0] + '/mainapp/model_files/indices.pkl')

# For SVD
book_cleaned_path = os.path.join(settings.STATICFILES_DIRS[0] + '/mainapp/dataset/books_cleaned.csv')
rating_pivot_path = os.path.join(settings.STATICFILES_DIRS[0] + '/mainapp/model_files/rating_pivot.csv.gz')
df = pd.read_csv(rating_pivot_path, index_col=0)
# Pivot table..
df.columns.name = df.index.name
df.index.name = df.index[0]
df_rating_pivot = df.iloc[1:]
# Rating Predictions
predictions_path = os.path.join(settings.STATICFILES_DIRS[0] + '/mainapp/model_files/predictions.npz')
predictions_npz = np.load(predictions_path)
predictions_array = predictions_npz['array1']
df_predictions = pd.DataFrame(predictions_array, columns=df_rating_pivot.columns)


cols = ['original_title', 'authors', 'average_rating', 'image_url', 'book_id']

df_book = pd.read_csv(book_path)
df_book_cleaned = pd.read_csv(book_cleaned_path)


def get_sorted_book_ids(predictions_df, userID, books_df):

    user_index = list(df_rating_pivot.index)
    # Get current user index
    pred_user_id = user_index.index(userID)

    # Get and sort the user's predictions
    user_row_number = pred_user_id
    sorted_book_ids = predictions_df.iloc[user_row_number].sort_values(ascending=False).index

    return sorted_book_ids


def get_book_title(bookid):
    '''
    Returns book title given bookid
    '''
    return df_book[df_book['book_id'] == bookid]['original_title'].values[0]


def get_book_ids(index_list):
    '''
    Returns bookids given list of indexes
    '''
    bookid_list = list(df_book.loc[index_list].book_id.values)
    return bookid_list


def get_rated_bookids(user_ratings):
    '''
    Returns list of already rated bookids
    '''
    already_rated = []
    for rating in user_ratings:
        book_id = rating.bookrating
        already_rated.append(book_id)
    return already_rated


def genre_wise(genre, percentile=0.85):
    available_genres_books = pd.read_csv("static/mainapp/dataset/genre.csv")
    df = available_genres_books[available_genres_books['genre'] == genre.lower()]
    qualified = pd.merge(df_book, df, left_on='book_id', right_on='book_id', how='inner')
    v = qualified['ratings_count']
    m = qualified['ratings_count'].quantile(percentile)
    R = qualified['average_rating']
    C = qualified['average_rating'].mean()
    qualified['weighted_rating'] = (R*v + C*m) / (v + m)
    qualified.sort_values('weighted_rating', ascending=False, inplace=True)
    return qualified[cols].head(16)


def count_vectorizer_recommendations(bookid):
    '''
        Returns recommened book ids based on book details
    '''
    indices = pd.read_pickle(book_indices_path)
    cosine_sim = np.load(cosin_sim_path)['array1']
    book_title = get_book_title(bookid)
    book_title = book_title.replace(' ', '').lower()
    idx = indices[book_title]

    # Get this books sim with all other books, enum to keep track of book index
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:10]

    book_indices = [i[0] for i in sim_scores]
    bookid_list = get_book_ids(book_indices)
    return bookid_list


def svd_recommendations(user_ratings):
    total_books = df_book_cleaned.shape[0]
    current_user_rating = np.zeros((1, total_books))

    for rating in user_ratings:
        bookid = rating.bookid
        rating = rating.bookrating
        # Since two separate datasets
        if bookid < total_books:
            current_user_rating[0][bookid] = rating

    # Find Closest user with similar rating
    df_user_rating = pd.DataFrame(current_user_rating, columns=[np.arange(1, total_books + 1)])
    distance = cdist(df_rating_pivot, df_user_rating, metric='euclidean')
    closest_user = df_rating_pivot[distance == distance.min()].index[0]

    # Get Sorted Book IDs
    sorted_book_ids = get_sorted_book_ids(df_predictions, closest_user, df_book_cleaned)

    return sorted_book_ids


def get_book_dict(bookid_list):
    '''
        Returns book details based on provided bookids
    '''
    rec_books_dict = df_book[df_book['book_id'].isin(bookid_list)][cols].to_dict('records')
    return rec_books_dict


def combine_ids(cv_bookids, svd_bookids, already_rated):
    '''
        Returns best bookids combining both approaches
    '''
    cv_bookids = list(cv_bookids.difference(already_rated))
    top_3_cv = set(cv_bookids[:3])
    svd_bookids = svd_bookids.difference(already_rated)
    svd_bookids = list(svd_bookids.difference(top_3_cv))
    top_6_svd = list(svd_bookids[:6])
    print(top_3_cv)
    print(top_6_svd)
    best_bookids = list(top_3_cv) + top_6_svd
    return best_bookids
