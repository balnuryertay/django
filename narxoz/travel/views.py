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

# def index(request):
#     posts = Travel.objects.all()
#
#     context = {
#         'posts': posts,
#         'menu': menu,
#         'title': 'Travel Land',
#         'cat_selected': 0,
#     }
#     return render(request, 'travel/index.html', context=context)

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

# def addpage(request):
#     if request.method == 'POST':
#         form = AddPostForm(request.POST, request.FILES)
#         if form.is_valid():
#             # print(form.cleaned_data)
#             form.save()
#             return redirect('home')
#     else:
#         form = AddPostForm()
#     return render(request, 'travel/addpage.html', {'form': form, 'menu': menu, 'title': 'Жаңалықтар'})

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

# def show_post(request, post_slug):
#     post = get_object_or_404(Travel, slug=post_slug)
#
#     context = {
#         'post': post,
#         'menu': menu,
#         'title': post.title,
#         'cat_selected': post.cat_id,
#     }
#
#     return render(request, 'travel/post.html', context=context)

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


# def show_category(request, cat_id):
#     posts = Travel.objects.filter(cat_id=cat_id)
#
#     if len(posts) == 0:
#         raise Http404()
#
#     context = {
#         'posts': posts,
#         'menu': menu,
#         'title': 'Категория бойынша көрсету',
#         'cat_selected': cat_id,
#     }
#     return render(request, 'travel/index.html', context=context)
