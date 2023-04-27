from django.urls import path, re_path
from django.views.decorators.cache import cache_page

from .views import *

urlpatterns = [
    path('', TravelHome.as_view(), name='home'),
    path('about/', about, name='about'),
    path('addpage/', AddPage.as_view(), name='add_page'),
    path('addagency/', AddAgency.as_view(), name='add_agency'),
    path('addagency/', AddContact.as_view(), name='contact'),
    path('contact/', ContactFormView.as_view(), name='contact'),
    path('tours/', TourHome.as_view(), name='tour'),
    path('qyzmet/', AgencyHome.as_view(), name='qyzmet'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('post/<slug:post_slug>/', ShowPost.as_view(), name='post'),
    path('agency/<slug:agency_slug>/', ShowAgency.as_view(), name='agency'),
    path('category/<slug:cat_slug>/', TravelCategory.as_view(), name='category')
]
