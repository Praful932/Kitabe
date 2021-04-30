from django.urls import reverse, resolve
from django.test import TestCase, Client
from mainapp import views
from django.contrib.auth.models import User
from mainapp.models import UserRating
from mainapp.helpers import most_common_genre_recommendations
from collections import Counter
import BookRecSystem.settings as settings
import random
import pandas as pd
import math
import os


class HomeTests(TestCase):
    '''
        Index View Test Case
    '''
    def setUp(self):
        self.url = reverse('index')

    def test_home_view_status_code(self):
        '''
            Index View Status Code
        '''
        response = self.client.get(self.url)
        self.assertEquals(response.status_code, 200)

    def test_home_url_resolves_home_view(self):
        '''
            Root URL Status Code
        '''
        view = resolve('/')
        self.assertEquals(view.func, views.index)


class GenreTestCase(TestCase):
    '''
        Genre View Test Case
    '''

    def setUp(self):
        self.genres = ['art', 'biography', 'business', 'Christian', 'Comics', 'Contemporary', 'Cookbooks', 'Crime',
                       'Fantasy', 'Fiction', 'History', 'Horror', 'Manga', 'Memoir', 'Mystery', 'Nonfiction',
                       'Paranormal', 'Philosophy', 'Poetry', 'Psychology', 'Religion', 'Science', 'Suspense',
                       'Spirituality', 'Sports', 'Thriller', 'Travel', 'Classics']

    def test_genre_status_code(self):
        '''
            All Genre Tests
        '''
        for genre in self.genres:
            url = reverse('genre_books', kwargs={'genre': genre})
            response = self.client.get(url)
            self.assertEquals(response.status_code, 200)


class ExploreTestCase(TestCase):
    '''
        Explore View Test Case
    '''

    def setUp(self):
        self.url = reverse('explore_books')

    def test_explore_status_code(self):
        '''
            Explore View Status Code
        '''
        response = self.client.get(self.url)
        self.assertEquals(response.status_code, 200)


class SearchAjaxTestCase(TestCase):
    '''
        AJAX Search View Test Case
    '''

    def setUp(self):
        self.url = reverse('search_ajax')

    def test_search_ajax_view_status_code(self):
        '''
            AJAX Test request with valid and invalid Book Name
        '''
        response = self.client.post(
            self.url,
            data={'bookName': 'Text'},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEquals(response.status_code, 200)
        self.assertIn('true', response.content.decode("utf-8"))

        response = self.client.post(
            self.url,
            data={},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEquals(response.status_code, 200)
        self.assertIn('false', response.content.decode("utf-8"))


class BookSummaryTestCase(TestCase):
    '''
        Book Summary View Test Case
    '''

    def setUp(self):
        self.url = reverse('summary_ajax')
        self.inputs = ['random_text', 1e10, ""]

    def test_book_summary_view_status_code(self):
        '''
            AJAX Test request with valid and invalid Book Id
        '''
        for ele in self.inputs:
            response = self.client.post(
                self.url,
                data={'bookid': ele},
                HTTP_X_REQUESTED_WITH='XMLHttpRequest'
            )
            self.assertEquals(response.status_code, 200)
            self.assertIn('false', response.content.decode("utf-8"))


class BookDetailsTestCase(TestCase):
    '''
        AJAX Book Details View Test Case
    '''

    def setUp(self):
        self.url = reverse('book_details')
        self.inputs = ['random_text', 1e10, ""]

    def test_book_details_view_status_code(self):
        '''
            AJAX Test request with valid and invalid Book Id
        '''
        for ele in self.inputs:
            response = self.client.post(
                self.url,
                data={'bookid': ele},
                HTTP_X_REQUESTED_WITH='XMLHttpRequest'
            )
            self.assertEquals(response.status_code, 200)
            self.assertIn('false', response.content.decode("utf-8"))


class UserRateBookTestCase(TestCase):
    '''
       AJAX User Rate Book Test Case
    '''

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='test_user', email='qwe@gmail.com')
        self.user.set_password('foopassword')
        self.user.save()
        self.url = reverse('user_rate_book')
        self.inputs = [('random_text', 7), (1e10, 5), ("", 1.0)]

    def test_user_rated_book_invalid(self):
        '''
            Test User Rates Book with invalid bookid
            with/out login
        '''
        for bookid, bookrating in self.inputs:
            response = self.client.post(
                self.url,
                data={'bookid': bookid,
                      'bookrating': bookrating},
                HTTP_X_REQUESTED_WITH='XMLHttpRequest'
            )
            self.assertEquals(response.status_code, 302)

        self.client.login(username='test_user', password='foopassword')
        for bookid, bookrating in self.inputs:
            response = self.client.post(
                self.url,
                data={'bookid': bookid,
                      'bookrating': bookrating},
                HTTP_X_REQUESTED_WITH='XMLHttpRequest'
            )
            self.assertEquals(response.status_code, 200)
            self.assertIn('false', response.content.decode("utf-8"))
        self.client.logout()

    def test_user_rated_book_valid(self):
        '''
            Test User Rates Book with valid bookid
            with/out login
        '''
        valid_book_id = 2
        valid_bookrating = 4

        response = self.client.post(
            self.url,
            data={'bookid': valid_book_id,
                  'bookrating': valid_bookrating},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEquals(response.status_code, 302)

        self.client.login(username='test_user', password='foopassword')

        response = self.client.post(
            self.url,
            data={'bookid': valid_book_id,
                  'bookrating': valid_bookrating},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEquals(response.status_code, 200)
        self.assertIn('true', response.content.decode("utf-8"))

        rating = UserRating.objects.get(bookid=valid_book_id)
        self.assertEquals(rating.bookrating, valid_bookrating)
        self.assertEquals(rating.user, self.user)
        self.client.logout()


class MostCommonGenreTestCase(TestCase):
    '''
    Test most common genre books when recommendations are short
    '''
    def setUp(self):
        self.df_book = pd.read_csv(os.path.join(settings.STATICFILES_DIRS[0] + '/mainapp/dataset/books.csv'))

    def common_genre(self, books):
        gfq = []
        for book in books:
            gfq.extend(self.df_book[self.df_book['book_id'] == book]['genre'].values[0].split(", "))
        genre_count = dict(Counter(gfq))
        max_value = max(genre_count.values())
        most_common_dict = {u: v for u, v in genre_count.items() if v == max_value}
        highest_book_count = {}
        for genre in most_common_dict.keys():
            highest_book_count[genre] = sum(self.df_book.genre.str.contains(genre.lower()))
        max_value = max(highest_book_count.values())
        final_dict = {u: v for u, v in highest_book_count.items() if v == max_value}
        most_common_genre = list(final_dict.items())[0][0]
        return most_common_genre

    def test(self):
        self.template(10, 5, 1)
        self.template(10, 5, 2)
        self.template(10, 5, 3)
        self.template(10, 5, 4)
        self.template(10, 5, 5)
        self.template(10, 6, 1)
        self.template(10, 6, 2)
        self.template(10, 6, 3)
        self.template(10, 6, 4)
        self.template(10, 7, 1)
        self.template(10, 7, 2)
        self.template(10, 7, 3)
        self.template(10, 8, 1)
        self.template(10, 8, 2)
        self.template(10, 9, 1)
        self.template(10, 10, 0)

    def template(self, tnum, already_slice, bestbookids_slice):
        books = random.sample(self.df_book.book_id.to_list(), tnum)
        already_rated = books[:already_slice]
        best_bookids = books[already_slice:already_slice+bestbookids_slice]
        n1 = math.ceil((9-len(best_bookids))/2)
        n2 = math.floor((9-len(best_bookids))/2)
        best_bookids_tfidf = books[tnum-n1+1:]

        genre_recomm_bookids = most_common_genre_recommendations(best_bookids, already_rated, best_bookids_tfidf, n2)
        genre = self.common_genre(best_bookids + already_rated + best_bookids_tfidf)

        for bookid in genre_recomm_bookids:
            self.assertEquals([False, genre][genre in self.df_book[self.df_book['book_id'] == bookid]['genre'].values[0].split(", ")], genre)


class RatedBooksTestCase(TestCase):
    """Already Read Books View Test Case"""
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='test_user', email='qwe@gmail.com')
        self.user.set_password('foopassword')
        self.user.save()
        self.url = reverse('read_books')

    def test_redirect_if_not_rated(self):
        """Test If The read_books Redirects
        Accordingly When No Book Is Rated
        """
        self.client.login(username='test_user', password='foopassword')
        response = self.client.get(self.url)
        self.assertRedirects(response, reverse('index'))
        self.client.logout()

    def test_read_book_status_code(self):
        """Test The Status Code Of read_books
        When Book Has Been Rated
        """
        self.userRating = UserRating.objects.create(user=self.user, bookid='2', bookrating='4')
        self.userRating.save()
        self.client.login(username='test_user', password='foopassword')
        response = self.client.get(self.url)
        self.assertEquals(response.status_code, 200)
        self.client.logout()
