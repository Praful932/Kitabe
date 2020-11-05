import pandas as pd
import numpy as np
import os
import pickle
import BookRecSystem.settings as settings

# For Count Vectorizer
book_path = os.path.join(settings.STATICFILES_DIRS[0] + '/mainapp/dataset/books.csv')
cosin_sim_path = os.path.join(settings.STATICFILES_DIRS[0] + '/mainapp/model_files/tf-idf/cosine_rating_sim.npz')
book_indices_path = os.path.join(settings.STATICFILES_DIRS[0] + '/mainapp/model_files/tf-idf/indices.pkl')

# For Embedding
book_id_map_path = os.path.join(settings.STATICFILES_DIRS[0] + '/mainapp/model_files/surprise/book_raw_to_inner_id.pickle')
book_raw_map_path = os.path.join(settings.STATICFILES_DIRS[0] + '/mainapp/model_files/surprise/book_inner_id_to_raw.pickle')
book_embed_path = os.path.join(settings.STATICFILES_DIRS[0] + '/mainapp/model_files/surprise/book_embedding.npy')
sim_books_path = os.path.join(settings.STATICFILES_DIRS[0] + '/mainapp/model_files/surprise/sim_books.pickle')

with open(book_id_map_path, 'rb') as handle:
    book_raw_to_inner_id = pickle.load(handle)

with open(book_raw_map_path, 'rb') as handle:
    book_inner_id_to_raw = pickle.load(handle)
book_embedding = np.load(book_embed_path)

with open(sim_books_path, 'rb') as handle:
    sim_books_dict = pickle.load(handle)


cols = ['original_title', 'authors', 'average_rating', 'image_url', 'book_id']

df_book = pd.read_csv(book_path)
total_books = df_book.shape[0]


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


def get_raw_id(book_id):
    '''
        Returns raw_id given book_id
    '''
    raw_id = df_book[df_book.book_id == book_id]['r_index'].values[0]
    return raw_id


def get_bookid(raw_id_list):
    '''
        Returns bookid list given rawid list
    '''
    bookid_list = list(df_book[df_book.r_index.isin(raw_id_list)]['book_id'].values)
    return bookid_list


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


def embedding_recommendations(sorted_user_ratings):
    '''
        Returns recommended book ids based on embeddings
    '''

    best_user_books = []
    similar_bookid_list = []

    for i, rating in enumerate(sorted_user_ratings):
        if rating.bookrating < 4 or i > 10:
            break
        else:
            best_user_books.append(rating.bookid)

    for book in best_user_books:
        raw_id = get_raw_id(book)
        top_sim_books = [book for book, similiarity in sim_books_dict[raw_id][:2]]
        similar_bookid_list.extend(top_sim_books)

    similar_bookid_list = get_bookid(similar_bookid_list)

    return similar_bookid_list


def get_book_dict(bookid_list):
    '''
        Returns book details based on provided bookids
    '''
    rec_books_dict = df_book[df_book['book_id'].isin(bookid_list)][cols].to_dict('records')
    return rec_books_dict


def combine_ids(cv_bookids, embedding_bookids, already_rated):
    '''
        Returns best bookids combining both approaches
    '''
    cv_bookids = list(cv_bookids.difference(already_rated))
    top_3_cv = set(cv_bookids[:2])
    embedding_bookids = embedding_bookids.difference(already_rated)
    embedding_bookids = list(embedding_bookids.difference(top_3_cv))
    top_3_cv = list(top_3_cv)
    top_6_embed = list(embedding_bookids[:7])
    print(top_3_cv)
    print(top_6_embed)
    best_bookids = top_3_cv + top_6_embed
    if len(best_bookids) < 9:
        best_bookids = best_bookids + cv_bookids[2:(len(9 - len(best_bookids)))]
    return best_bookids


def select_random_books():
    df_books1 = df_book.copy()
    v = df_books1['ratings_count']
    m = df_books1['ratings_count'].quantile(0.95)
    R = df_books1['average_rating']
    C = df_books1['average_rating'].mean()
    W = (R*v + C*m) / (v + m)
    df_books1['weighted_rating'] = W
    qualified = df_books1.sort_values(
        'weighted_rating', ascending=False)[cols].head(90)
    return qualified.to_dict('records')
