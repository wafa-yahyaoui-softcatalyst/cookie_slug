from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView

from .models import Post
from .forms import PostForm


class PostListView(ListView):

    model = Post
    template_name = 'blog/post_list.html'


class PostDetailView(DetailView):

    model = Post
    template_name = 'blog/post_detail.html'


class PostCreate(CreateView):
    form_class = PostForm
    model = Post
    template_name = 'blog/post_create.html'
    success_url = '/'

    def form_valid(self, form):
        model = form.save(commit=False)
        model.author = self.request.user
        model.published_date = timezone.now()
        model.save()
        return super(PostCreate, self).form_valid(form)


class PostUpdate(UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_edit.html'
    success_url = '/'
    def form_valid(self, form):
        model = form.save(commit=False)
        model.author = self.request.user
        model.published_date = timezone.now()
        model.save()
        return super(PostUpdate, self).form_valid(form)
