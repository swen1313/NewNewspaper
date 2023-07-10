from datetime import datetime

from django.shortcuts import render
from django.views.generic import ListView, DetailView, DeleteView, UpdateView, CreateView
from .filters import PostFilter

from .fotms import PostForm
from .models import Post


class PostList(ListView):
    model = Post
    template_name = 'news.html'
    context_object_name = 'news'
    queryset = Post.objects.order_by('datetime')
    paginate_by = 1


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()

        return context


class PostDetail(DetailView):
    model = Post
    template_name = 'news_detail.html'
    context_object_name = 'post'
    queryset = Post.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['datetime'] = datetime.utcnow()
        return context

class PostDeleteView(DeleteView):
    template_name = 'news_delete.html'
    queryset = Post.objects.all()
    success_url = '/news'


class PostUpdateView(UpdateView):
    template_name = 'news_create.html'
    form_class = PostForm
    success_url = '/news'

    def get_object(self, **kwargs):
            id = self.kwargs.get('pk')
            return Post.objects.get(pk=id)


class PostCreateView(CreateView):
    template_name = 'news_create.html'
    form_class = PostForm
    success_url = '/news'

# Create your views here.
class PostSearchList(ListView):
    model = Post
    template_name = 'news_search.html'
    context_object_name = 'news'
    queryset = Post.objects.order_by('datetime')
    paginate_by = 1


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset())

        return context
