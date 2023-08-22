from typing import Any, Dict
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.views import View
from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView
from django.core.paginator import Paginator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.urls import reverse_lazy
from .filters import PostFilter
from .forms import PostForm
from .models import Post, Author, Category
from django.shortcuts import redirect
from django.urls import resolve
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.core.exceptions import PermissionDenied
from django.core.exceptions import ValidationError
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.http import HttpResponse
from datetime import timedelta
import datetime
from django.utils import timezone




class PostList(ListView):
    model = Post
    ordering = ['-creationData']
    template_name = 'post/posts.html'
    context_object_name = 'posts'
    paginate_by = 2

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
        return super().get(request, *args, **kwargs)
    

class PostSearch(ListView):
    model = Post
    ordering = ['-creationData']
    template_name = 'post/post_search.html'
    context_object_name = 'post_search'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = PostFilter(self.request.GET, queryset = self.get_queryset())
        context['form'] = PostForm()
        return context


class PostDetail(DetailView):
    model = Post
    template_name = 'post/post.html'
    context_object_name = 'post'
    queryset = Post.objects.all()


class PostCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Post
    template_name = 'post/post_create.html'
    permission_required = ('news.add_post',
                            'news.change_post')
    permission_denied_message = 'Чтобы создавать новости, необходимо стать автором'
    form_class = PostForm


    def form_valid(self, form):
        super().form_valid(form)
        author = Author.objects.get(authorUser=self.object.author.authorUser)
        yesterday = timezone.now() - timedelta(days=1)
        posts_day = Post.objects.filter(author=author, creationData__gt=yesterday)
        print(posts_day)
        if posts_day.count() > 3:
            posts_day.last().delete()
            raise ValidationError("You can't post more than 3 news per day")
        else:
            return redirect('/news/')
        

class PostUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    template_name = 'post/post_create.html'
    permission_required = ('news.add_post',
                            'news.change_post')
    permission_denied_message = 'Чтобы редактировать новости, необходимо стать автором'
    form_class = PostForm

    def get_object(self, **kwargs):
       id = self.kwargs.get('pk')
       return Post.objects.get(pk=id)


class PostDeleteView(DeleteView):
    template_name = 'post/post_delete.html'
    queryset = Post.objects.all()
    success_url = reverse_lazy('news:all_posts')


class ProfileView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'profile/profile.html'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        category = Category.objects.all().filter(subscribers=user)
        context['category'] = category
        context['is_not_authors'] = not self.request.user.groups.filter(name = 'authors').exists()
        return context
    

@login_required
def upgrade_me(request):
    user = request.user
    Author.objects.create(authorUser=user)
    premium_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        premium_group.user_set.add(user)
    return redirect('/news/')


class HomeView(TemplateView):
    template_name = 'post/home_page.html'


class CategoriesView(ListView):
    model = Category
    template_name = 'post/categories.html'
    context_object_name = 'categories'
    queryset = Category.objects.all()


class PostCategoryView(ListView):
    model = Post
    template_name = 'post/category.html'
    context_object_name = 'posts'

    def get_queryset(self):
        self.id = resolve(self.request.path_info).kwargs['pk']
        cat = Category.objects.get(id=self.id)
        queryset = Post.objects.filter(postCategory = cat).order_by('-creationData')
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        category = Category.objects.get(id=self.id)
        context['category'] = category
        context['subscribed'] = category.subscribers.filter(id=user.id)
        return context 


@login_required
def subscribe_to_category(request, pk):
    user = request.user
    category = Category.objects.get(id=pk)

    if not category.subscribers.filter(id=user.id).exists():
        category.subscribers.add(user)
        email = user.email
        html = render_to_string(
            'mail/subscribe.html',
            context={
                'category': category,
                'user': user,
            },
        )

        msg = EmailMultiAlternatives(
            subject=f'{category} subscription',
            body='',
            from_email='geographsawqa@yandex.ru',
            to=[email,],
        )

        msg.attach_alternative(html, 'text/html')

        try:
            msg.send()
        except Exception as e:
            print(e)
        return redirect('news:profile')
    return redirect(request.META.get('HTTP_REFERER'))


@login_required
def unsubscribe_to_category(request, pk):
    user = request.user
    category = Category.objects.get(id=pk)

    if category.subscribers.filter(id=user.id).exists():
        category.subscribers.remove(user)
    return redirect('news:profile')
    
