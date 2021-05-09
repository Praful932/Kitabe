from django.db import models
from django.contrib.auth.models import User
from mainapp.helpers import get_book_title

import BookRecSystem.settings as settings
import pandas as pd
import os

book_path = os.path.join(settings.STATICFILES_DIRS[0] + '/mainapp/dataset/books.csv')
df_book = pd.read_csv(book_path)


class UserRating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_rating')
    bookid = models.IntegerField()
    bookrating = models.IntegerField()

    def __str__(self):
        return self.user.username.capitalize() + '- ' + get_book_title(self.bookid) + '  - ' + str(self.bookrating)


class SaveForLater(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bookid = models.IntegerField()

    def __str__(self):
        return self.user.username.capitalize() + '- ' + get_book_title(self.bookid)
