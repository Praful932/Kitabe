from django.db import models
from django.contrib.auth.models import User
# Create your models here.

# class UserProfile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
    
#     def __str__(self):
#         return f'{self.user.username} Profile'

class UserRating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name= 'user_rating')
    bookid = models.IntegerField()
    bookrating = models.IntegerField()

    def __str__(self):
        return self.user.username.capitalize() + ' Bookid : ' +  str(self.bookid)
