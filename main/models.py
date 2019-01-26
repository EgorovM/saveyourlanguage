from __future__                     import unicode_literals
from django.utils.encoding          import python_2_unicode_compatible
from django.db                      import models
from django.contrib.auth.models     import User
from django.utils 					import timezone
from django 						import forms

class Profile(models.Model):
	user  = models.OneToOneField(User)
	score = models.IntegerField(default = 0)

	def __str__(self):
		return str(self.user)