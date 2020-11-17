from __future__                     import unicode_literals
from django.db                      import models
from django.contrib.auth.models     import User
from django.utils 					import timezone
from django 						import forms

class Profile(models.Model):
    user      = models.OneToOneField(User, on_delete=models.CASCADE)
    name      = models.CharField(max_length = 30)
    score     = models.IntegerField(default = 0)

    def __str__(self):
        return str(self.user)


class Image(models.Model):
    way       = models.CharField(max_length = 600)
    author    = models.CharField(max_length = 500)
    label     = models.BooleanField(default = 0)
    letter    = models.CharField(max_length=1)
    def __str__(self):
        return str(self.author)
