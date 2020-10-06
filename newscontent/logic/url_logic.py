from django.shortcuts import render, HttpResponse, redirect
from .ajax_requests.likes import likes_control
from django.views.generic import ListView, DetailView, View
from django.views.generic.edit import CreateView
from ..models import Section, New, Rate
from ..forms import NewForm, LoginForm, SearchForm
from news.settings import BASE_DIR
from random import choice
import json
from django.core.paginator import Paginator
from django.contrib.sites.models import Site
from django.contrib.auth import authenticate, login
from django.contrib.auth.views import (LogoutView, LoginView, PasswordResetView,
                                       PasswordResetDoneView, PasswordResetCompleteView, PasswordResetConfirmView)

data_rates = str(BASE_DIR) + '/newscontent/logic/api/data_files/data_rates.json'
data_weather = str(BASE_DIR) + '/newscontent/logic/api/data_files/data_weather.json'

from django.contrib.sites.models import Site


class ContextAbstract:
    current_site = Site.objects.get_current()
    main_url = "http://" + current_site.domain

    @staticmethod
    def abstract_context(request):
        with open(data_rates, 'r') as file:
            valute = dict(json.loads(file.read()))
        with open(data_weather, 'r')as file:
            cities = dict(json.loads(file.read()))
            city = choice(list(cities.keys()))
            temp = cities[city]

        main_valutes = ['USD', 'EUR', 'CNY']
        rates = Rate.objects.all()  # Валюты
        sections = Section.objects.all()  # Разделы новостей
        last5 = New.objects.all().order_by('-date')[:5]
        abs_context = {"city": city, "temp": temp, "valute": valute, "main_valutes": main_valutes, "rates": rates,
                       "sections": sections, "main_url": ContextAbstract.main_url,
                       "authenticated": request.user.is_authenticated,
                       "user": request.user.username, "search_form": SearchForm, "last5": last5}

        return abs_context


class MainView(View, ContextAbstract):
    def get(self, request):

        context = {}
        context.update(super().abstract_context(request))
        return render(request, 'main_page.html', context)


class NewList(ListView, ContextAbstract):
    model = New
    template_name = 'news_list.html'
    paginate_by = 10

    def check_sort_field(self):
        if 'sort_field' in self.request.POST.keys():
            return New.objects.filter(section__title=self.kwargs['section_title']).order_by(
                self.request.POST['sort_field'])
        else:
            return New.objects.filter(section__title=self.kwargs['section_title'])

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['logged'] = self.request.user.is_authenticated
        # context['page_obj'] = self.check_sort_field()
        context['current_section'] = Section.objects.get(title=self.kwargs['section_title'])
        context.update(super().abstract_context(self.request))

        return context

    def get_queryset(self):
        if 'sort_field' in self.request.GET:
            return New.objects.filter(section__title=self.kwargs['section_title']).order_by(
                self.request.GET['sort_field'])
        return New.objects.filter(section__title=self.kwargs['section_title'])


class NewDetail(DetailView, ContextAbstract):
    model = New
    context_object_name = 'news'
    template_name = 'new_detail.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_new'] = New.objects.get(id=self.kwargs['pk'])
        text_len = len(New.objects.get(id=self.kwargs['pk']).text)
        if New.objects.get(id=self.kwargs['pk']).picture:
            textend_part1 = int(text_len / 3)
            textend_part2 = textend_part1 * 2
            context['text_part1'] = New.objects.get(id=self.kwargs['pk']).text[:textend_part1] + '-'
            context['text_part2'] = New.objects.get(id=self.kwargs['pk']).text[textend_part1:textend_part2] + '-'
            context['text_part3'] = New.objects.get(id=self.kwargs['pk']).text[textend_part2:]

        context.update(super().abstract_context(self.request))
        return context


class NewCreate(CreateView, ContextAbstract):
    form_class = NewForm
    model = New
    template_name = 'create_new.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_section'] = Section.objects.get(title=self.kwargs['title'])
        context.update(super().abstract_context(self.request))
        return context


class LogView(LoginView):

    def get_context_data(self, **kwargs):
        new_context = super().get_context_data(**kwargs)
        new_context.update(ContextAbstract.abstract_context(self.request))
        return new_context


class PasswordResView(PasswordResetView):
    template_name = 'registration/password_rst.html'

    def get_context_data(self, **kwargs):
        new_context = super().get_context_data(**kwargs)
        new_context.update(ContextAbstract.abstract_context(self.request))
        return new_context


class PasswordResDoneView(PasswordResetDoneView):
    template_name = 'registration/password_rst_done.html'

    def get_context_data(self, **kwargs):
        new_context = super().get_context_data(**kwargs)
        new_context.update(ContextAbstract.abstract_context(self.request))
        return new_context


class PasswordResConfirmView(PasswordResetConfirmView):
    template_name = 'registration/password_rst_confirm.html'

    def get_context_data(self, **kwargs):
        new_context = super().get_context_data(**kwargs)
        new_context.update(ContextAbstract.abstract_context(self.request))
        return new_context


class PasswordResCompleteView(PasswordResetCompleteView):
    template_name = 'registration/password_rst_complete.html'

    def get_context_data(self, **kwargs):
        new_context = super().get_context_data(**kwargs)
        new_context.update(ContextAbstract.abstract_context(self.request))
        return new_context
