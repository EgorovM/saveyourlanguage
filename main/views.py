from django.shortcuts 			import render, HttpResponseRedirect, redirect
from .models					import Profile, Image
from django.utils 				import timezone
from django.db 					import IntegrityError
from django.core.paginator 		import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.models import User
from django.contrib.auth 		import authenticate
from django.contrib.auth 		import logout
from django.contrib 			import auth
from django.utils 				import timezone
from django.core.files.base import ContentFile
from django.core.files.storage import FileSystemStorage
import datetime
import json
from io import StringIO
import threading
import base64
import time

AVATAR_SIZE  = (254, 169)
PICTURE_SIZE = (500, 500)

def ajax(request):
	if request.method == 'POST': # and request.FILES['image']:
		image_data = request.POST['image']
		letter     = request.POST['letter']

		format, imgstr = image_data.split(';base64,')
		ext = format.split('/')[-1]
		data = ContentFile(base64.b64decode(imgstr))
		myfile = letter + "/" + str(request.user.profile.name) + "-"+time.strftime("%Y%m%d-%H%M%S")+"." + ext
		fs = FileSystemStorage()
		filename = fs.save(myfile, data)

		profile = Profile.objects.get(user = request.user)
		profile.score += 1
		profile.save()

	request = render(request, 'main/index.html')

	return request
    

def resizeImage(file, size):
	imagefile  = StringIO.StringIO(file.read())
	image      = Image.open(imagefile)

	image.thumbnail(size, Image.ANTIALIAS)

	imagefile = StringIO.StringIO()
	image.save(imagefile, 'PNG')

	file.file = imagefile

	return file

def index(request):
	if request.user.is_authenticated():
		profile = request.user.profile
	else:
		return redirect('login')

	context = {"profile": profile}

	response = render(request, 'main/index.html',context)

	return response

def profile(request,profile_id):
	if not request.user.is_authenticated():
		return redirect('login')

	error_message = None

	profile = Profile.objects.get(id = profile_id)

	if request.method == "POST":
		if "ok_button" in request.POST:
			new_post_text = request.POST["new_post_text"]

			if new_post_text == "":
				error_message = "Напишите что-нибудь"
			else:
				post = Post()
				post.data   = timezone.now()
				post.text   = new_post_text
				post.author = request.user.profile
				post.status = "post"
				post.save()

		if "delete" in request.POST:
			post = Post.objects.get(id = request.POST["post_id"])
			post.delete()

			return HttpResponseRedirect('.')

	posts   = Post.objects.filter(author = profile, status = "post")[::-1]
	context = {"posts": posts}

	context["profile"]       = request.user.profile
	context["view_profile"]  = profile
	context["error_message"] = error_message
	response = render(request, 'main/profile.html',context)

	return response

def settings(request):
	if not request.user.is_authenticated():
		return redirect('login')

	error_message = None

	context = {"profile":request.user.profile,}

	if request.method == "POST":
		if "ok_button" in request.POST:
			new_name  	  = request.POST["name"]
			new_email 	  = request.POST["email"]
			new_telephone = request.POST["telephone"]

			profile = Profile.objects.get(user = request.user)

			profile.name  	        = new_name
			profile.user.email      = new_email
			profile.telephone       = new_telephone

			profile.save()
			profile.user.save()

	response = render(request, 'main/index.html',context)

	return response


def picture(request):

	if not request.user.is_authenticated():
		return redirect('login')

	error_message = None

	context = {"profile":request.user.profile,}

	if request.method == "POST":
		if "ok_button" in request.POST:
			profile = Profile.objects.get(user = request.user)

			new_image = ""

			if "image" in request.FILES:
				new_image = request.FILES["image"]
				profile.photo = new_image
				profile.save()

				return HttpResponseRedirect(".")
			else:
				error_message = "Нет"
				context["error_message"] = error_message

	response = render(request, 'main/picture.html',context)

	return response

def group(request):
	if not request.user.is_authenticated():
		return redirect('login')
		
	context = {}

	context["profile"] = request.user.profile

	twelfth_hum = Profile.objects.filter(grade = "11ГУМ")
	context["twelfth_hum"] = twelfth_hum

	twelfth_biochem = Profile.objects.filter(grade = "11БХ")
	context["twelfth_biochem"] = twelfth_biochem

	twelfth_politech = Profile.objects.filter(grade = "11ПТХ")
	context["twelfth_politech"] = twelfth_politech

	twelfth_tech = Profile.objects.filter(grade = "11ТЕХ")
	context["twelfth_tech"] = twelfth_tech

	twelfth_engeneer = Profile.objects.filter(grade = "11ИНЖ")
	context["twelfth_engeneer"] = twelfth_engeneer

	twelfth_physmath = Profile.objects.filter(grade = "11ФМ")
	context["twelfth_physmath"] = twelfth_physmath

	response = render(request, 'main/group.html',context)

	return response

def login(request):
	if request.user.is_authenticated():
		return redirect('/')
		

	false_message = None

	if request.method == "POST":
		if "ok_button" in request.POST:
			login    = request.POST["login"]
			password = request.POST["password"]

			if login != "" and password != "":
				user = authenticate(username = login, password = password)

				if user is not None and user.is_active:
					auth.login(request, user)
					return HttpResponseRedirect("/feed")
				else:
					false_message = "Неправильный логин или пароль"
			else:
				false_message = "Неправильно введены данные"
		if "register" in request.POST:
			return redirect("/register")

	context = {"false_message":false_message}

	response = render(request, 'main/login.html',context)

	return response

def register(request):
	error_message = None
	context = {}

	if request.method == "POST":
		if "ok_button" in request.POST:

			username = request.POST["username"]
			password = request.POST["password"]
			name     = request.POST["name"]

			if username !='' and password !='':
				if  len(password) < 8:
					error_message = "Длина пароля не менее 8 символов"
				else:
					try:
						user = User.objects.create_user(username = username, password = password)
						user.save()

					except IntegrityError:
						error_message = "Не удалось зарегистрировать"
						response = render(request, 'main/register.html',{"error_message":error_message})
						return response

					profile = Profile(user = user)
					profile.name = name
					profile.save()      

					user = authenticate(username = username, password = password)

					if user is not None and user.is_active:
						auth.login(request, user)
						return HttpResponseRedirect("/")
					else:
						error_message = "Пользователь уже существует"
						context["error_message"] = error_message
			else:
				error_message = "Поле не должно быть пустым"

				response = render(request, 'main/register.html',{"error_message":error_message})
				return response

	response = render(request, 'main/register.html',context)

	return response

def logout_view(request):

	logout(request)

	return HttpResponseRedirect("/login")