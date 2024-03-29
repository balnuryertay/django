from django.db import models
from django.urls import reverse
from rest_framework.authtoken.admin import User


class Travel(models.Model):
    title = models.CharField(max_length=255, verbose_name="Travel")
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")
    content = models.TextField(blank=True, verbose_name="Анықтама")
    photo = models.ImageField(upload_to="photos/%Y/%m/%d/", verbose_name="Фото")
    price = models.TextField(blank=True, verbose_name="Бағасы")
    time_create = models.DateTimeField(auto_now_add=True, verbose_name="Сақталған уақыты")
    time_update = models.DateTimeField(auto_now=True, verbose_name="Өзгертілген уақыты")
    is_published = models.BooleanField(default=True, verbose_name="Публикация")
    cat = models.ForeignKey('Category', on_delete=models.PROTECT, verbose_name="Категориясы")
    user = models.ForeignKey(User, verbose_name='Пайдаланушы', on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post', kwargs={'post_slug': self.slug})

    class Meta:
        verbose_name = 'Саяхат'
        verbose_name_plural = 'Саяхаттар'
        ordering = ['-time_create', 'title']

class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True, verbose_name="Категория")
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category', kwargs={'cat_slug': self.slug})

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категориялар'
        ordering = ['id']

class Travel_Agency(models.Model):
    title = models.CharField(max_length=255, verbose_name="Tour Agency")
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")
    content = models.TextField(blank=True, verbose_name="Анықтама")
    photo = models.ImageField(upload_to="photos/%Y/%m/%d/", verbose_name="Фото")
    time_create = models.DateTimeField(auto_now_add=True, verbose_name="Сақталған уақыты")
    time_update = models.DateTimeField(auto_now=True, verbose_name="Өзгертілген уақыты")
    is_published = models.BooleanField(default=True, verbose_name="Публикация")
    user = models.ForeignKey(User, null=True, verbose_name='Пайдаланушы', on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('agency', kwargs={'agency_slug': self.slug})

    class Meta:
        verbose_name = 'Тур агенттік'
        verbose_name_plural = 'Тур агенттіктер'
        ordering = ['-time_create', 'title']

class Contact(models.Model):
    title = models.CharField(max_length=255, verbose_name="Name")
    email = models.CharField(max_length=255, verbose_name="Email")
    content = models.TextField(blank=True, verbose_name="Анықтама")
    captcha = models.TextField(blank=True)
    time_create = models.DateTimeField(auto_now_add=True, verbose_name="Сақталған уақыты")
    time_update = models.DateTimeField(auto_now=True, verbose_name="Өзгертілген уақыты")
    is_published = models.BooleanField(default=True, verbose_name="Публикация")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('contact', kwargs={'contact_slug': self.slug})

    class Meta:
        verbose_name = 'Байланыс'
        verbose_name_plural = 'Байланыстар'
        ordering = ['-time_create', 'title']