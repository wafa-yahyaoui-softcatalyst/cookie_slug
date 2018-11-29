from django.utils import timezone
from django.core.mail import send_mail
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, FormView
from django.shortcuts import get_object_or_404, redirect
from django.http import JsonResponse
from django.shortcuts import render
from django.core import serializers
from .models import Post
from .forms import PostForm, FeedbackForm


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
    template_name = 'blog/post_detail.html'
    success_url = '/'

    def form_valid(self, form):
        model = form.save(commit=False)
        model.author = self.request.user
        model.published_date = timezone.now()
        model.save()
        return super(PostUpdate, self).form_valid(form)

    def get(self, request, *args, **kwargs):
        if self.request.is_ajax():
            return JsonResponse({'title': self.get_object().title,
                                 'text': self.get_object().text})

        return super(PostUpdate, self).get(request, *args, **kwargs)


class Feedback(FormView):
    form_class = FeedbackForm
    template_name = 'blog/feedback.html'
    success_url = '/'

    def form_valid(self, form):
        # mail_to_send = form.save(commit=False)
        send_mail(
            'Subject: Feedback',
            form.cleaned_data['feedback'],
            form.cleaned_data['email'],
            ['to@example.com'],
            fail_silently=False,
        )

        return super(Feedback, self).form_valid(form)


def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})

# AJAX with class based views
