from django.utils import timezone
from django.core.mail import send_mail
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, FormView, DeleteView
from django.shortcuts import get_object_or_404, redirect
from django.http import JsonResponse
from django.shortcuts import render
from django.core import serializers
from django.http import HttpResponse
import json
from .models import Post
from .forms import PostForm, FeedbackForm
from django.views.generic import View


class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'

    def get(self, request, *args, **kwargs):
        if self.request.is_ajax():
            results = [ob.as_json() for ob in Post.objects.all()]
            return HttpResponse(json.dumps(results, indent=4, sort_keys=True, default=str),
                                content_type="application/json")

        return super(PostListView, self).get(request, *args, **kwargs)


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
            my_object = self.get_object()
            return JsonResponse({'title': my_object.title,
                                 'text': my_object.text})

        return super(PostUpdate, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        response = super(PostUpdate, self).post(request, *args, **kwargs)
        if self.request.is_ajax():
            return JsonResponse({'message': 'success'})
        return response


class PostDelete(View):

    def post(self, request, *args, **kwargs):
        response = super(PostDelete, self).__init__(*args, **kwargs)
        if self.request.is_ajax():
            Post.objects.get(pk=request.POST['pk']).delete()
            return JsonResponse({'message': 'success'})
        return response


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
