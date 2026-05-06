from django.contrib.auth import logout, login
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView

from main_blog.forms import AddPostForm, RegisterUserForm, LoginUserForm
from main_blog.models import Article, Category
from main_blog.utils import DataMixin

menu = [
    {'title': 'Главная', 'url_name': 'home'},
    {'title': 'Добавить статью', 'url_name': 'add_page'},
    {'title': 'О сайте', 'url_name': 'about'},
    {'title': 'Авторизация', 'url_name': 'login'}
]

# def index(request):
#     posts = Article.objects.exclude(slug='').filter(is_published=True)
#     cats = Category.objects.all()
#     return render(request, 'main_blog/index.html', {'posts': posts, 'title': 'Главная свэг', 'menu': menu, 'category': cats}, )

class BlogHome(DataMixin, ListView):
    model = Article
    template_name = 'main_blog/index.html'
    context_object_name = 'posts'
    def get_context_data(self, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title = 'Главная страница')
        return dict(list(context.items()) + list(c_def.items()))
    #делаем фильтр чтобы показывало только опубликованные статьи
    def get_queryset(self):
        return Article.objects.filter(is_published=True)

def about(request):
    return render(request, 'main_blog/about.html', {'menu': menu})

# def add_page(request):
#     #проверяем что если форму создали, то мы выводим данные в консоль, а если нет, то пустая форма
#     if request.method == 'POST':
#         form = AddPostForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             return redirect('home')
#     else:
#         form = AddPostForm()
#     form = AddPostForm()
#     return render(request, 'main_blog/add_page.html', {'form':form, 'menu': menu, 'title': 'Добавление статьи'})

class AddPage(LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddPostForm
    template_name = 'main_blog/add_page.html'
    #делаем редирект на домашнюю страницу после заполения формы
    success_url = reverse_lazy('home')

    login_url = '/admin/'
    def get_context_data(self, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Добавление статьи')
        return dict(list(context.items()) + list(c_def.items()))


# def show_post(request, post_slug):
#     post = get_object_or_404(Article, slug=post_slug)
#     context = {'post': post, 'menu': menu, 'title': post.title, 'cat_selected': post.cat.slug}
#
#     return render(request, 'main_blog/post.html', context = context)

class ShowPost(DataMixin, DetailView):
    model = Article
    template_name = 'main_blog/post.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'

    def get_context_data(self, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title=context['post'])
        return dict(list(context.items()) + list(c_def.items()))

# def show_category(request, cat_slug):
#     the_cat = Category.objects.get(slug=cat_slug)
#     posts = Article.objects.filter(cat_id=the_cat.id)
#     cats = Category.objects.all()
#     #if len(posts) == 0:
#         #raise  Http404
#     return render(request, 'main_blog/index.html',
#                   {'posts': posts, 'title': 'Главная свэг', 'menu': menu, 'category': cats}, )

class BlogCategory(DataMixin, ListView):
    model = Article
    template_name = 'main_blog/index.html'
    context_object_name = 'posts'
    #не разрешаем открывать старницу если нет данных, выдавать 404
    allow_empty = False
    def get_context_data(self, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Категория - ' + str(context['posts'][0].cat),
                                      cat_selected=context['posts'][0].cat_id)
        return dict(list(context.items()) + list(c_def.items()))

    #делаем фильтр чтобы показывало только опубликованные статьи
    def get_queryset(self):
        return Article.objects.filter(cat__slug = self.kwargs['cat_slug'], is_published=True)

def categories(request):
    return HttpResponse("Тут будут категории")

class RegisterUser(DataMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'main_blog/register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Регистрация")
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')

class LoginUser(DataMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'main_blog/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Авторизация")
        return dict(list(context.items()) + list(c_def.items()))

    def get_success_url(self):
        return reverse_lazy('home')

def logout_user(request):
    logout(request)
    return redirect('login')

def pageNotFound(request, exception):
    return HttpResponseNotFound(f'<h1>Такой страницы нет</h1><p>{exception}</p>')