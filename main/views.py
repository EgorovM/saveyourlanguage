from django.shortcuts 			import render, HttpResponseRedirect, redirect
from .models					import Profile
from django.utils 				import timezone
from django.db 					import IntegrityError
from django.core.paginator 		import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.models import User
from django.contrib.auth 		import authenticate
from django.contrib.auth 		import logout
from django.contrib 			import auth
from django.utils 				import timezone
from PIL      					import Image
import datetime
import json
from io import StringIO
import threading

def authenticate_user(request):	
	login    = request.POST["username"]
	password = request.POST["password"]

	feedback = None

	if login != "" and password != "":
		user = authenticate(username = login, password = password)

		if user is not None and user.is_active:
			auth.login(request, user)
			feedback = "Успешно вошли"
		else:
			feedback = "Неправильный логин или пароль"
	else:
		feedback = "Неправильно введены данные"

	return feedback

def index(request):
	context = {}

	if request.method == "POST":
		if "login_btn" in request.POST:
			feedback = authenticate_user(request)
			context["feedback"] = feedback

	request = render(request, 'main/index.html', context)

	return request


def begin(request):
	context = {}

	request = render(request, 'main/index', context)

	return request


def results(request):
	context = {}

	request = render(request, 'main/index', context)

	return request