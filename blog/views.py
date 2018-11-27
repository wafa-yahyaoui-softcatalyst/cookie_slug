from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView

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


def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})
