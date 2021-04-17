import pandas as pd
import numpy as np
import os
import pickle
import operator
import random
import BookRecSystem.settings as settings
import mainapp.models

book_path = os.path.join(settings.STATICFILES_DIRS[0] + '/mainapp/dataset/books.csv')

# For Count Vectorizer
cosin_sim_path = os.path.join(settings.STATICFILES_DIRS[0] + '/mainapp/model_files/cv/cosine_rating_sim.npz')
book_indices_path = os.path.join(settings.STATICFILES_DIRS[0] + '/mainapp/model_files/cv/indices.pkl')

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


def is_rating_invalid(rating):
    if not rating or not rating.isdigit():
        return True
    if int(rating) > 5:
        return True
    return False


def is_bookid_invalid(bookid):
    if not bookid or not bookid.isdigit():
        return True
    elif sum(df_book['book_id'] == int(bookid)) == 0:
        # If bookid does not exist
        return True
    return False


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
        book_id = rating.bookid
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
    '''
        Returns top genre books according to a cutoff percentile to be listed in Top Books
    '''
    n_books = 16
    min_genre_book_count = 48

    qualified = df_book[df_book.genre.str.contains(genre.lower())]
    # Imdb Formula
    v = qualified['ratings_count']
    m = qualified['ratings_count'].quantile(percentile)
    R = qualified['average_rating']
    C = qualified['average_rating'].mean()
    W = (R*v + C*m) / (v + m)
    qualified = qualified.assign(weighted_rating=W)
    qualified.sort_values('weighted_rating', ascending=False, inplace=True)

    return qualified[cols].head(min_genre_book_count).sample(n_books)


def count_vectorizer_recommendations(bookid):
    '''
        Returns recommened book ids based on book details
    '''
    indices = pd.read_pickle(book_indices_path)
    cosine_sim = np.load(cosin_sim_path)['array1']
    book_title = get_book_title(bookid)
    book_title = book_title.replace(' ', '').lower()
    idx = indices[book_title]

    # Get this books similarity with all other books, enum to keep track of book index
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
    max_user_rating_len = 10
    # Only keep user rating >= 4
    threshold = 4
    top_similiar = 2

    for i, rating in enumerate(sorted_user_ratings):
        if rating.bookrating < threshold or i > max_user_rating_len:
            break
        else:
            best_user_books.append(rating.bookid)

    for book in best_user_books:
        raw_id = get_raw_id(book)
        top_sim_books = [book for book, similiarity in sim_books_dict[raw_id][:top_similiar]]
        similar_bookid_list.extend(top_sim_books)

    similar_bookid_list = get_bookid(similar_bookid_list)

    return similar_bookid_list


def get_book_dict(bookid_list):
    '''
        Returns book details based on provided bookids
    '''
    rec_books_dict = df_book[df_book['book_id'].isin(bookid_list)][cols].to_dict('records')
    return rec_books_dict


def combine_ids(cv_bookids, embedding_bookids, already_rated, recommendations=9):
    '''
        Returns best bookids combining both approaches
        Embedding - Top 6
        CV - Top 3
    '''
    cv_bookids = list(cv_bookids.difference(already_rated))
    top_3_cv = set(cv_bookids[:3])
    embedding_bookids = embedding_bookids.difference(already_rated)
    embedding_bookids = list(embedding_bookids.difference(top_3_cv))
    top_3_cv = list(top_3_cv)
    top_6_embed = list(embedding_bookids[:6])
    best_bookids = top_3_cv + top_6_embed

    if len(best_bookids) < recommendations:
        # If not enough recommendations
        best_bookids = best_bookids + cv_bookids[3:(recommendations + 3 - len(best_bookids))]
    return best_bookids


def get_top_n(top_n=400):
    """
        Returns a sample of top N books
    """
    df_books_copy = df_book.copy()
    v = df_books_copy['ratings_count']
    m = df_books_copy['ratings_count'].quantile(0.95)
    R = df_books_copy['average_rating']
    C = df_books_copy['average_rating'].mean()
    W = (R*v + C*m) / (v + m)
    df_books_copy = df_books_copy.assign(weighted_rating=W)
    qualified = df_books_copy.sort_values(
        'weighted_rating', ascending=False)[cols].head(top_n)
    return qualified.sample(top_n)


def popular_among_users(N=15):
    '''
        Returns Popular Books Among Users in the
        rating range 4-5.
        If enough books are not available, top books are
        sampled randomly.
    '''
    all_ratings = list(mainapp.models.UserRating.objects.all().order_by('-bookrating'))
    random.shuffle(all_ratings)
    best_user_ratings = sorted(all_ratings, key=operator.attrgetter('bookrating'), reverse=True)

    filtered_books = set()
    for i, rating in enumerate(best_user_ratings):
        if rating.bookrating >= 4:
            filtered_books.add((rating.bookid))
        elif rating.bookrating < 4 or len(filtered_books) == N:
            break

    remaining_books_nos = N - len(filtered_books)
    if remaining_books_nos >= 0:
        rem_books = get_top_n(2*N)['book_id'].tolist()
        filtered_books = list(filtered_books) + list((set(rem_books) - filtered_books))[:remaining_books_nos]

    return get_book_dict(filtered_books)
