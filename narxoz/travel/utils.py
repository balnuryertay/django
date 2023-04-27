from django.db.models import Count
from django.core.cache import cache

from .models import *

menu = [
    {'title':"Басты бет",'url_name':'home'},
    {'title':"Біз туралы",'url_name':'about'},
    {'title':"Тур агенттіктер",'url_name':'qyzmet'},
    {'title':"Турлар",'url_name':'tour'},
    {'title':"Байланыс", 'url_name':'contact'}]

class DataMixin:
    paginate_by = 20

    def get_user_context(self, **kwargs):
        context = kwargs
        cats = cache.get('cats')
        if not cats:
            cats = Category.objects.annotate(Count('travel'))
            cache.set('cats', cats, 60)

        user_menu = menu.copy()
        if not self.request.user.is_authenticated:
            user_menu.pop(1)

        context['menu'] = menu

        context['cats'] = cats
        if 'cat_selected' not in context:
            context['cat_selected'] = 0
        return context
