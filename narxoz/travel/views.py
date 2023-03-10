from django.http import HttpResponse, HttpResponseNotFound, Http404, HttpResponseServerError, HttpResponseForbidden, \
    HttpResponseBadRequest
from django.shortcuts import render, redirect, get_object_or_404

from .forms import *
from .models import *

menu = [
    {'title':"Біз туралы",'url_name':'about'},
    {'title':"Тур агенттіктер",'url_name':'home'},
    {'title':"Байланыс", 'url_name':'contact'},
    {'title':"Логин", 'url_name':'login'}]

def index(request):
    posts = Travel.objects.all()

    context = {
        'posts': posts,
        'menu': menu,
        'title': 'Travel Land',
        'cat_selected': 0,
    }
    return render(request, 'travel/index.html', context=context)

def about(request):
    return render(request, 'travel/about.html', {'menu': menu, 'title': 'About us'})

def addpage(request):
    if request.method == 'POST':
        form = AddPostForm(request.POST)
        if form.is_valid():
            # print(form.cleaned_data)
            try:
                Travel.objects.create(**form.cleaned_data)
                return redirect('home')
            except:
                form.add_error(None, 'Пост құруда қателіктер кетті')
    else:
        form = AddPostForm()
    return render(request, 'travel/addpage.html', {'form': form, 'menu': menu, 'title': 'Жаңалықтар'})

def contact(request):
    return HttpResponse('Обратная связь')

def login(request):
    return HttpResponse('Авторизация')

def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>404<br>Страница не найдена</h1>')

def serverError(request):
    return HttpResponseServerError('<h1>500<br>Ошибка сервера</h1>')

def forbidden(request, exception):
    return HttpResponseForbidden('<h1>403<br>Доступ запрещен</h1>')

def badRequest(request, exception):
    return HttpResponseBadRequest('<h1>400<br>Невозможно обработать запрос</h1>')

def show_post(request, post_slug):
    post = get_object_or_404(Travel, slug=post_slug)

    context = {
        'post': post,
        'menu': menu,
        'title': post.title,
        'cat_selected': post.cat_id,
    }

    return render(request, 'travel/post.html', context=context)

def show_category(request, cat_id):
    posts = Travel.objects.filter(cat_id=cat_id)

    if len(posts) == 0:
        raise Http404()

    context = {
        'posts': posts,
        'menu': menu,
        'title': 'Категория бойынша көрсету',
        'cat_selected': cat_id,
    }
    return render(request, 'travel/index.html', context=context)
