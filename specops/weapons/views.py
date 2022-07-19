from unicodedata import category
from django.http import Http404, HttpResponse, HttpResponseNotFound
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, FormView, TemplateView
from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.core.paginator import Paginator

from .forms import *
from .models import *
from .utils import *

class WeaponsHome(DataMixin,ListView):
    model = Weapon
    template_name = 'weapons/index.html'
    context_object_name = 'posts'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title = 'Главная страница')
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        return Weapon.objects.filter(is_published=True).select_related('cat')

class AboutSite(DataMixin, TemplateView):
    template_name = 'weapons/about.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title = 'О сайте')
        return dict(list(context.items()) + list(c_def.items()))

class AddPage(LoginRequiredMixin ,DataMixin, CreateView):
    form_class = AddPostForm
    template_name = 'weapons/addpage.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title = 'Добавление статьи')
        return dict(list(context.items()) + list(c_def.items()))


class ContactFormView(DataMixin, FormView):
    form_class = ContactForm
    template_name = 'weapons/contact.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Обратная связь")
        return dict(list(c_def.items()) + list(context.items()))

    def form_valid(self, form):
        print(form.cleaned_data)
        return redirect('home')


class ShowPost(DataMixin,DetailView):
    model = Weapon
    template_name = 'weapons/post.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title = context['post'])
        return dict(list(context.items()) + list(c_def.items()))


class WeaponsCategory(DataMixin,ListView):
    model = Weapon
    template_name = 'weapons/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c = Category.objects.get(slug=self.kwargs['cat_slug'])
        c_def = self.get_user_context(title = 'Категория - ' + str(c.name),
                                      cat_selected = c.pk)
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        return Weapon.objects.filter(cat__slug=self.kwargs['cat_slug'], is_published=True).select_related('cat')


def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')

class RegisterUser(DataMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'weapons/register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title = "Регистрация")
        return dict(list(context.items()) + list(c_def.items()))
    
    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')

class LoginUser(DataMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'weapons/login.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title = 'Авторизация')
        return dict(list(context.items()) + list(c_def.items()))
    
    def get_success_url(self):
        return reverse_lazy('home')


def logout_user(request):
    logout(request)
    return redirect('login')