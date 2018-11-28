from django.utils import timezone
from django.core.mail import send_mail
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, FormView

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
    template_name = 'blog/post_edit.html'
    success_url = '/'

    def form_valid(self, form):
        model = form.save(commit=False)
        model.author = self.request.user
        model.published_date = timezone.now()
        model.save()
        return super(PostUpdate, self).form_valid(form)


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
