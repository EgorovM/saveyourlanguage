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
from django.http import JsonResponse
import datetime
import json
from io import StringIO
import threading
import base64
from django.conf import settings
import time
import os

import tensorflow as tf
import cv2
import numpy as np
import glob


AVATAR_SIZE  = (254, 169)
PICTURE_SIZE = (500, 500)

ALL_LETTERS = ['Б', 'Ф', 'Ж', 'У', 'Ъ', 'П', 'Э', 'И', 'Ь', 'Ы', 'О', 'З', 'Ү',
               'Т', 'А', 'Х', 'Ё', 'Й', '-', 'h', 'Е', 'Р', 'В', 'Ч', 'Ю', 'Л',
               'Щ', 'М', 'Ш', 'Н', 'ҥ', 'ө', 'Я', 'К', 'Г', 'Ц', 'Д', 'С', 'Ҕ']

model = tf.keras.models.load_model(settings.BASE_DIR + '/sakhaREC.h5')


def prepare_image(way):
    img = cv2.imread(way)
    img_gray = (255 - cv2.cvtColor(img, cv2.COLOR_BGR2GRAY))

    return cv2.resize(img_gray / 255, (28, 28))


def predict(rec):
    rec = 1 - rec
    print(rec.mean())

    pred = list(model.predict(np.reshape(rec, (-1, 28, 28)))[0])
    max_prob = max(pred)

    print(max_prob)
    return ALL_LETTERS[pred.index(max_prob)]


def ajax(request):
    context = {}

    if request.method == 'POST': # and request.FILES['image']:
        image_data = request.POST['image']
        letter     = request.POST['letter']
        save = request.POST.get('save', False)
        print(save, type(save), save=='false')
        profile = Profile.objects.get(user = request.user)
        profile.score += 1
        profile.save()

        format, imgstr = image_data.split(';base64,')
        ext = format.split('/')[-1]
        data = ContentFile(base64.b64decode(imgstr))
        myfile = letter + "/" + str(profile.name) + "-"+time.strftime("%Y%m%d-%H%M%S")+"." + ext
        fs = FileSystemStorage()
        filename = fs.save(myfile, data)

        rec = prepare_image('media/' + myfile)

        img = Image(
        	way=myfile,
        	author=profile.name,
        	letter=letter,
        )

        predicted_letter = predict(rec)

        if save == 'false':
            print('delete...')
            os.remove(os.path.join(settings.MEDIA_ROOT, img.way))
        else:
            img.save()


        return JsonResponse({"letter": predicted_letter, "ok": predicted_letter == letter})

    request = render(request, 'main/index.html', context)

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
    if request.user.is_authenticated:
    	profile = Profile.objects.get(user=request.user)
    else:
    	return redirect('login')

    context = {"profile": profile}

    response = render(request, 'main/index.html',context)

    return response


def check(request):
	data = {}
	images = Image.objects.filter(label=0)
	data["images"] = images

	if request.method == "POST":
		img_id = request.POST["id"]
		img = Image.objects.get(id = img_id)

		if "ok" in request.POST:
			img.label = 1
			img.save()
		if "not" in request.POST:
			os.remove(os.path.join(settings.MEDIA_ROOT, img.way))
			img.delete()

	return render(request, 'main/check.html', data)


def login(request):
	if request.user.is_authenticated:
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


def for_children(request):
    ALL_LETTERS = list(map(lambda x: x[-1:], glob.glob("../handmade/*")))

    response = render(request, 'main/for_children.html', locals())

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
