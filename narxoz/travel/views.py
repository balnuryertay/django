from django.contrib.auth import logout, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.core.paginator import Paginator
from django.forms import model_to_dict
from django.http import HttpResponse, HttpResponseNotFound, Http404, HttpResponseServerError, HttpResponseForbidden, \
    HttpResponseBadRequest
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework import generics, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser, IsAuthenticated
from rest_framework.viewsets import GenericViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView

from .forms import *
from .models import *
from .permissions import IsAdminOrReadOnly, IsOwnerOrReadOnly
from .serializers import TravelSerializer
from .utils import *

class TravelHome(DataMixin, ListView):
    model = Travel
    template_name = 'travel/index.html'
    context_object_name = 'posts'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Басты бет")
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        return Travel.objects.filter(is_published=True).select_related('cat')


class AddPage(LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddPostForm
    template_name = 'travel/addpage.html'
    success_url = reverse_lazy('home')
    login_url = reverse_lazy('home')
    raise_exception = True

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Мақала қосу")
        return dict(list(context.items()) + list(c_def.items()))


class ShowPost(DataMixin, DetailView):
    model = Travel
    template_name = 'travel/post.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title=context['post'])
        return dict(list(context.items()) + list(c_def.items()))



class TravelCategory(DataMixin, ListView):
    model = Travel
    template_name = 'travel/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_queryset(self):
        return Travel.objects.filter(cat__slug=self.kwargs['cat_slug'], is_published=True).select_related('cat')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c = Category.objects.get(slug=self.kwargs['cat_slug'])
        c_def = self.get_user_context(title='Категория - ' + str(c.name),
                                      cat_selected=c.pk)
        return dict(list(context.items()) + list(c_def.items()))


class RegisterUser(DataMixin, CreateView):
    form_class = UserCreationForm
    template_name = 'travel/register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Регистрация')
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')


class LoginUser(DataMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'travel/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Авторизация')
        return dict(list(context.items()) + list(c_def.items()))

    def get_success_url(self):
        return reverse_lazy('home')

def logout_user(request):
    logout(request)
    return redirect('login')

def about(request):
    contact_list = Travel.objects.all()
    paginator = Paginator(contact_list, 3)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'travel/about.html', {'page_obj': page_obj, 'menu': menu, 'title': 'About us'})

class ContactFormView(DataMixin, FormView):
    form_class = ContactForm
    template_name = 'travel/contact.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Обратная связь")
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        print(form.cleaned_data)
        return redirect('home')


class TravelAPIListPagination(PageNumberPagination):
    page_size = 3
    page_size_query_param = 'page_size'
    max_page_size = 10000

class TravelAPIList(generics.ListCreateAPIView):
    queryset = Travel.objects.all()
    serializer_class = TravelSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, )
    pagination_class = TravelAPIListPagination

class TravelAPIUpdate(generics.RetrieveUpdateAPIView):
    queryset = Travel.objects.all()
    serializer_class = TravelSerializer
    permission_classes = (IsAuthenticated, )
    # authentication_classes = (TokenAuthentication, )

class TravelAPIDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Travel.objects.all()
    serializer_class = TravelSerializer
    permission_classes = (IsAdminOrReadOnly, )

# def login(request):
#     return HttpResponse('Авторизация')

# class TravelAPIList(generics.ListCreateAPIView):
#     queryset = Travel.objects.all()
#     serializer_class = TravelSerializer
#
# class TravelAPIUpdate(generics.UpdateAPIView):
#     queryset = Travel.objects.all()
#     serializer_class = TravelSerializer
#
# class TravelAPIDetailView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Travel.objects.all()
#     serializer_class = TravelSerializer

# class TravelAPIView(APIView):
#     def get(self, request):
#         t = Travel.objects.all()
#         return Response({'posts': TravelSerializer(t, many=True).data})
#
#     def post(self, request):
#         serializer = TravelSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#
#         return Response({'post': serializer.data})
#
#     def put(self, request, *args, **kwargs):
#         pk = kwargs.get("pk", None)
#         if not pk:
#             return Response({"error": "Method PUT not allowed"})
#
#         try:
#             instance = Travel.objects.get(pk=pk)
#         except:
#             return Response({"error": "Object does not exists"})
#
#         serializer = TravelSerializer(data=request.data, instance=instance)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response({"post": serializer.data})
#
#     def delete(self, request, *args, **kwargs):
#         pk = kwargs.get("pk", None)
#         if not pk:
#             return Response({"error": "Method PUT not allowed"})
#
#         return Response({"post": "delete post " + str(pk)})


def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>404<br>Страница не найдена</h1>')

def serverError(request):
    return HttpResponseServerError('<h1>500<br>Ошибка сервера</h1>')

def forbidden(request, exception):
    return HttpResponseForbidden('<h1>403<br>Доступ запрещен</h1>')

def badRequest(request, exception):
    return HttpResponseBadRequest('<h1>400<br>Невозможно обработать запрос</h1>')