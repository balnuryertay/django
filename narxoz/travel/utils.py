from django.db.models import Count
from django.core.cache import cache

from .models import *

menu = [
    {'title':"Біз туралы",'url_name':'about'},
    {'title':"Тур агенттіктер",'url_name':'home'},
    # {'title':"Барлық категориялар",'url_name':'category/<slug:cat_slug>'},
    {'title':"Қызметтер",'url_name':'qyzmet'},
    {'title':"Байланыс", 'url_name':'contact'},
    {'title':"Логин", 'url_name':'login'}]

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
