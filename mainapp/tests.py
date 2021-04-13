from django.urls import reverse, resolve
from django.test import TestCase, Client
from mainapp import views
from django.contrib.auth.models import User
from mainapp.models import UserRating


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
