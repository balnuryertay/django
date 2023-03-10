from django import forms
from .models import *

class AddPostForm(forms.Form):
    title = forms.CharField(max_length=255, label="title")
    slug = forms.SlugField(max_length=255, label="url")
    content = forms.CharField(widget=forms.Textarea(attrs={'cols': 60, 'rows': 10}), label="text")
    is_published = forms.BooleanField(label="posts", required=False, initial=True)
    cat = forms.ModelChoiceField(queryset=Category.objects.all(), label="categories", empty_label="категория таңдалынбады")

