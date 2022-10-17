import pandas as pd
import numpy as np
import os
import math
import pickle
import operator
import random
from collections import Counter
import BookRecSystem.settings as settings
import mainapp.models

book_path = os.path.join(settings.STATICFILES_DIRS[0] + "/mainapp/dataset/books.csv")

# For Count Vectorizer
cosine_sim_path = os.path.join(
    settings.STATICFILES_DIRS[0] + "/mainapp/model_files/tf-idf/cosine_rating_sim.npz"
)
book_indices_path = os.path.join(
    settings.STATICFILES_DIRS[0] + "/mainapp/model_files/tf-idf/indices.pkl"
)

# For Embedding
book_id_map_path = os.path.join(
    settings.STATICFILES_DIRS[0]
    + "/mainapp/model_files/surprise/book_raw_to_inner_id.pickle"
)
book_raw_map_path = os.path.join(
    settings.STATICFILES_DIRS[0]
    + "/mainapp/model_files/surprise/book_inner_id_to_raw.pickle"
)
book_embed_path = os.path.join(
    settings.STATICFILES_DIRS[0] + "/mainapp/model_files/surprise/book_embedding.npy"
)
sim_books_path = os.path.join(
    settings.STATICFILES_DIRS[0] + "/mainapp/model_files/surprise/sim_books.pickle"
)

with open(book_id_map_path, "rb") as handle:
    book_raw_to_inner_id = pickle.load(handle)

with open(book_raw_map_path, "rb") as handle:
    book_inner_id_to_raw = pickle.load(handle)
book_embedding = np.load(book_embed_path)

with open(sim_books_path, "rb") as handle:
    sim_books_dict = pickle.load(handle)

cols = ["original_title", "authors", "average_rating", "image_url", "book_id"]

df_book = pd.read_csv(book_path)
total_books = df_book.shape[0]


def is_rating_invalid(rating):
    """Return a boolean value.

    Checks if the rating is invalid.

    Parameters
    ----------
    rating : int
        Rating of a book, which should be a digit <= 5.

    Returns
    -------
    bool
        `True` if the rating is invalid, else `False`.

    """
    if not rating or not rating.isdigit():
        return True
    if int(rating) > 5:
        return True
    return False


def is_bookid_invalid(bookid):
    """Return a boolean value.

    Checks if the bookid is invalid.

    Parameters
    ----------
    bookid : int
        book-id of the book to be checked for existence.

    Returns
    -------
    bool
        `True` if the bookid exists, else `False`.

    """
    if not bookid or not bookid.isdigit():
        return True
    elif sum(df_book["book_id"] == int(bookid)) == 0:
        # If bookid does not exist
        return True
    return False


def get_book_title(bookid):
    """Return book title given bookid.

    Parameters
    ----------
    bookid : int
        book-id of a book whose title needs to be determined.

    Returns
    -------
    bookname : str
        Title of the book corresponding the given book id.

    """
    return df_book[df_book["book_id"] == bookid]["original_title"].values[0]


def get_book_ids(index_list):
    """Return bookids given list of indexes.

    Parameters
    ----------
    index_list : list
        List of indexes for which the book-ids are to be determined.

    Returns
    -------
    bookid_list : list
        List of bookids corresponding to given list of indexes.

    """
    bookid_list = list(df_book.loc[index_list].book_id.values)
    return bookid_list


def get_rated_bookids(user_ratings):
    """Return list of already rated bookids.

    Parameters
    ----------
    user_ratings : list
        List of ratings by the users.

    Returns
    -------
    already_rated : list
        List of book-ids, corresponding to the books already rated by the users.

    """
    already_rated = []
    for rating in user_ratings:
        book_id = rating.bookid
        already_rated.append(book_id)
    return already_rated


def get_raw_id(book_id):
    """Return raw_id given book_id.

    Parameters
    ----------
    book_id : int
        Integer to determine the raw-id of a book.

    Returns
    -------
    raw_id : int
        Corresponding raw_id of the book_id.

    """
    raw_id = df_book[df_book.book_id == book_id]["r_index"].values[0]
    return raw_id


def get_bookid(raw_id_list):
    """Return bookid list given rawid list.

    Parameters
    ----------
    raw_id_list : list
        List containing raw-ids to determine respective book-ids.

    Returns
    -------
    bookid_list : list
        List of bookids corresponding to raw ids.

    """
    bookid_list = list(df_book[df_book.r_index.isin(raw_id_list)]["book_id"].values)
    return bookid_list


def genre_wise(genre, percentile=0.85):
    """Return top genre books according to a cutoff percentile.

    Parameters
    ----------
    genre : str
        Genre of the book in string format.

    percentile : float
         Float determinig the cutoff percentile (Default value = `0.85`).

    Returns
    -------
    df : pandas.core.frame.DataFrame
        Top genre books according to a cutoff percentile.

    """
    n_books = 16
    min_genre_book_count = 48

    qualified = df_book[df_book.genre.str.contains(genre.lower())]
    # Imdb Formula
    v = qualified["ratings_count"]
    m = qualified["ratings_count"].quantile(percentile)
    R = qualified["average_rating"]
    C = qualified["average_rating"].mean()
    W = (R * v + C * m) / (v + m)
    qualified = qualified.assign(weighted_rating=W)
    qualified.sort_values("weighted_rating", ascending=False, inplace=True)

    return qualified[cols].head(min_genre_book_count).sample(n_books)


def tfidf_recommendations(bookid):
    """Return recommenedations based on count vectorizer.

    Parameters
    ----------
    bookid : int
        Integer which needs to be passed in order to get book-title.

    Returns
    -------
    bookid_list : list
        List of bookids based on count vectorizer.

    """
    indices = pd.read_pickle(book_indices_path)
    cosine_sim = np.load(cosine_sim_path)["array1"]
    book_title = get_book_title(bookid)
    book_title = book_title.replace(" ", "").lower()
    idx = indices[book_title]

    # Get this books similarity with all other books, enum to keep track of book index
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:10]

    book_indices = [i[0] for i in sim_scores]
    bookid_list = get_book_ids(book_indices)
    return bookid_list


def embedding_recommendations(sorted_user_ratings):
    """Return recommended book ids based on embeddings.

    Parameters
    ----------
    sorted_user_ratings : list
        List containing the ratings given by user.

    Returns
    -------
    similar_bookid_list : list
        A list of recommended book ids based on embeddings.

    """
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
        top_sim_books = [
            book for book, similiarity in sim_books_dict[raw_id][:top_similiar]
        ]
        similar_bookid_list.extend(top_sim_books)

    similar_bookid_list = get_bookid(similar_bookid_list)

    return similar_bookid_list


def get_book_dict(bookid_list):
    """Return book details based on provided bookids.

    Parameters
    ----------
    bookid_list : list
        List containing book-ids which needs to be passed to determine book-details.

    Returns
    -------
    rec_books_dict : dict
        Dictionary of book details based on provided list of bookids.

    """
    rec_books_dict = df_book[df_book["book_id"].isin(bookid_list)][cols].to_dict(
        "records"
    )
    return rec_books_dict


def combine_ids(tfidf_bookids, embedding_bookids, already_rated, recommendations=9):
    """Return best bookids combining both approaches.

        Embedding - Top 6
        Tf-Idf - Top 3

    Parameters
    ----------
    tfidf_bookids : list
        List containing book-ids of books based on Tf-Idf.

    embedding_bookids : list
        List containing book-ids of books rated by users.

    already_rated : list
        List containing book-ids of already rated books.

    recommendations : int
         Integer denoting the number of recommendations (Default value = 9).

    Returns
    -------
    best_bookids : list
        List containing bookids of top books based on embeddings and tfidf.

    """
    tfidf_bookids = list(tfidf_bookids.difference(already_rated))
    top_3_tfidf = set(tfidf_bookids[:3])
    embedding_bookids = embedding_bookids.difference(already_rated)
    embedding_bookids = list(embedding_bookids.difference(top_3_tfidf))
    top_3_tfidf = list(top_3_tfidf)
    top_6_embed = list(embedding_bookids[:6])
    best_bookids = top_3_tfidf + top_6_embed

    # If not enough recommendations
    if len(best_bookids) < recommendations:
        two_n = recommendations - len(best_bookids)
        # Divide remaining recommendations into two parts
        n1, n2 = math.ceil(two_n / 2), math.floor(two_n / 2)

        # n1 number of books from remaining tf_idf books
        best_bookids_tfidf = tfidf_bookids[3 : (3 * 2) + n1]
        best_bookids_tfidf = list(
            set(best_bookids_tfidf).difference(set(best_bookids))
        )[:n1]

        # n2 number of books from list of top rated books of the most common genre among the books yet recommended
        genre_recomm_bookids = most_common_genre_recommendations(
            best_bookids + already_rated + best_bookids_tfidf, n2
        )

        # number of recommendations = len(best_bookids) + n1 + n2 = len(best_bookids) + two_n
        best_bookids = best_bookids + best_bookids_tfidf + genre_recomm_bookids
    return best_bookids


def most_common_genre_recommendations(books, n):
    """Returns n top rated of the most_common_genre among all lists taken as input

    Parameters
    ----------
    books : list
        List of books to find common genre for
    n : int
        Integer denoting the number of books required (Default value = 9).
    Returns
    -------
    genre_recommendations : list
        List containing n number of books of the most common genre among all the input books.
    """

    # Accumulation of all the genres listed from books
    genre_frequency = []
    for book in books:
        genre_frequency.append(
            df_book[df_book["book_id"] == book]["genre"].values[0].split(", ")[0]
        )

    most_common_genre = sorted(Counter(genre_frequency).most_common())[0][0]

    # Recommendations list, listing 2n bookids
    genre_recommendations = genre_wise(most_common_genre).book_id.to_list()[: 2 * n]
    # Removing common bookids from `books` and Slicing out the first n bookids
    genre_recommendations = list(set(genre_recommendations).difference(books))[:n]

    return genre_recommendations


def get_top_n(top_n=400):
    """Return a sample of top N books based on weighted average ratings.

    Parameters
    ----------
    top_n : int
         Number of samples to be returned (Default value = 400).

    Returns
    -------
    df : pandas.core.frame.DataFrame
        Sample of top N books.

    """
    df_books_copy = df_book.copy()
    v = df_books_copy["ratings_count"]
    m = df_books_copy["ratings_count"].quantile(0.95)
    R = df_books_copy["average_rating"]
    C = df_books_copy["average_rating"].mean()
    W = (R * v + C * m) / (v + m)
    df_books_copy = df_books_copy.assign(weighted_rating=W)
    qualified = df_books_copy.sort_values("weighted_rating", ascending=False)[
        cols
    ].head(top_n)
    return qualified.sample(top_n)


def popular_among_users(N=15):
    """Return Popular Books Among Users in the rating range 4-5.

        If enough books are not available, top books are
        sampled randomly.

    Parameters
    ----------
    N : int
         Number of samples to be returned (Default value = 15).

    Returns
    -------
    book_details : dict
        Dictionary of book details.

    """
    all_ratings = list(mainapp.models.UserRating.objects.all().order_by("-bookrating"))
    random.shuffle(all_ratings)
    best_user_ratings = sorted(
        all_ratings, key=operator.attrgetter("bookrating"), reverse=True
    )

    filtered_books = set()
    for i, rating in enumerate(best_user_ratings):
        if rating.bookrating >= 4:
            filtered_books.add(rating.bookid)
        elif rating.bookrating < 4 or len(filtered_books) == N:
            break

    remaining_books_nos = N - len(filtered_books)
    if remaining_books_nos >= 0:
        rem_books = get_top_n(2 * N)["book_id"].tolist()
        filtered_books = (
            list(filtered_books)
            + list(set(rem_books) - filtered_books)[:remaining_books_nos]
        )

    return get_book_dict(filtered_books)
