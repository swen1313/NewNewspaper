from datetime import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, DeleteView, UpdateView, CreateView, TemplateView
from .filters import PostFilter
from .fotms import PostForm

from .models import Post, Category


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_authors'] = not self.request.user.groups.filter(name='authors').exists()
        return context





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


class PostUpdateView(UpdateView, LoginRequiredMixin, PermissionRequiredMixin):
    template_name = 'news_create.html'
    form_class = PostForm
    success_url = '/news'
    permission_required =('newspaper.change_post')

    def get_object(self, **kwargs):
            id = self.kwargs.get('pk')
            return Post.objects.get(pk=id)


class PostCreateView(CreateView, PermissionRequiredMixin):
    template_name = 'news_create.html'
    form_class = PostForm
    success_url = '/news'
    permission_required = ('newspaper.add_post')

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


@login_required
def subscribers(request):
    if request.method == 'POST' and request.POST['category']:
        category = get_object_or_404(Category, pk=request.POST['category'])
        user = get_object_or_404(User, pk=request.POST['user_pk'])
        if not category.subscribers.filter(pk=user.pk):
            category.subscribers.add(user)
            category.save()
            messages.success(request, f'Вы успешно подписались на категорию "{category}" !')
        else:
            messages.error(request, 'Вы подписывались на эту категорию ранее !')
        return redirect('news', category_pk=request.POST['category'])
    return redirect('news')







