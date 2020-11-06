from django.urls import reverse, resolve
from django.test import TestCase
from mainapp import views


class HomeTests(TestCase):
    def test_home_view_status_code(self):
        url = reverse('index')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_home_url_resolves_home_view(self):
        view = resolve('/')
        self.assertEquals(view.func, views.index)


class GenreTestCase(TestCase):
    def test_genre_status_code(self):
        genres = ['art', 'biography', 'business', 'Christian', 'Comics', 'Contemporary', 'Cookbooks', 'Crime',
                  'Fantasy', 'Fiction', 'History', 'Horror', 'Manga', 'Memoir', 'Mystery', 'Nonfiction',
                  'Paranormal', 'Philosophy', 'Poetry', 'Psychology', 'Religion', 'Science', 'Suspense',
                  'Spirituality', 'Sports', 'Thriller', 'Travel', 'Classics']
        for genre in genres:
            url = reverse('genre_books', kwargs={'genre': genre})
            response = self.client.get(url)
            self.assertEquals(response.status_code, 200)


class ExploreTestCase(TestCase):
    def explore_status_code(self):
        url = reverse('explore_books')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
