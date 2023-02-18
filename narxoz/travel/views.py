from django.http import HttpResponse, HttpResponseNotFound, Http404, HttpResponseServerError, HttpResponseForbidden, \
    HttpResponseBadRequest
from django.shortcuts import render, redirect

from .models import *

menu = ["Біз туралы", "Тур агенттіктер", "Байланыс", "Логин"]

def index(request):
    posts = Travel.objects.all()
    return render(request, 'travel/index.html', {'posts': posts, 'menu': menu, 'title': 'Travel Land'})

def about(request):
    return render(request, 'travel/about.html', {'menu': menu, 'title': 'About us'})

def categories(request, catid):
    if(request.POST):
        print(request.POST)

    return HttpResponse(f"<h1>Статьи по категориям</h1><p>{catid}</p>")

def archive(request, year):
    if int(year) > 2023:
        return redirect('home', permanent=True)
        # raise Http404()
    if int(year) < 1990:
        return HttpResponseForbidden('<h1>403<br>Доступ запрещен</h1>')

    return HttpResponse(f"<h1>Архив по годам</h1><p>{year}</p>")

def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>404<br>Страница не найдена</h1>')

def serverError(request):
    return HttpResponseServerError('<h1>500<br>Ошибка сервера</h1>')

def forbidden(request, exception):
    return HttpResponseForbidden('<h1>403<br>Доступ запрещен</h1>')

def badRequest(request, exception):
    return HttpResponseBadRequest('<h1>400<br>Невозможно обработать запрос</h1>')
