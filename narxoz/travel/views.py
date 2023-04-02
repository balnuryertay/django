from django.http import HttpResponse, HttpResponseNotFound, Http404, HttpResponseServerError, HttpResponseForbidden, \
    HttpResponseBadRequest
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView

from .forms import *
from .models import *

menu = [
    {'title':"Біз туралы",'url_name':'about'},
    {'title':"Тур агенттіктер",'url_name':'home'},
    # {'title':"Барлық категориялар",'url_name':'category/<slug:cat_slug>'},
    {'title':"Қызметтер",'url_name':'qyzmet'},
    {'title':"Байланыс", 'url_name':'contact'},
    {'title':"Логин", 'url_name':'login'}]

class TravelHome(ListView):
    model = Travel
    template_name = 'travel/index.html'
    context_object_name = 'posts'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = menu
        context['title'] = 'Басты бет'
        context['cat_selected'] = 0
        return context

    def get_queryset(self):
        return Travel.objects.filter(is_published=True)

def about(request):
    return render(request, 'travel/about.html', {'menu': menu, 'title': 'About us'})

class AddPage(CreateView):
    form_class = AddPostForm
    template_name = 'travel/addpage.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Мақала қосу'
        context['menu'] = menu
        return context

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

class ShowPost(DetailView):
    model = Travel
    template_name = 'travel/post.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = context['post']
        context['menu'] = menu
        return context

class TravelCategory(ListView):
    model = Travel
    template_name = 'travel/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_queryset(self):
        return Travel.objects.filter(cat__slug=self.kwargs['cat_slug'], is_published=True)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Категория - ' + str(context['posts'][0].cat)
        context['menu'] = menu
        context['cat_selected'] = context['posts'][0].cat_id
        return context
