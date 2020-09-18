from django.http import HttpResponse
from django.shortcuts import render
from .ajax_requests.likes import likes_control_ajax
from .api.valute_weather import clear_dts, api_weather_rates
from django.views.generic import ListView, DetailView, View
from django.views.generic.edit import CreateView
from ..models import Section, New
from ..forms import NewForm
from news.settings import BASE_DIR
from random import choice
import json

data_rates = str(BASE_DIR) + '/newscontent/logic/api/data_files/data_rates.json'
data_weather = str(BASE_DIR) + '/newscontent/logic/api/data_files/data_weather.json'


class ContextAbstract:

    @staticmethod
    def update_context():
        with open(data_rates, 'r') as file:
            valute = dict(json.loads(file.read()))
        with open(data_weather, 'r')as file:
            cities = dict(json.loads(file.read()))
            city = choice(list(cities.keys()))
            temp = cities[city]

            abs_context = {"city": city, "temp": temp, "valute": valute}

        return abs_context


class MainView(View, ContextAbstract):
    def get(self, request):
        sections = Section.objects.all()
        with open(data_rates, 'r') as file:
            valute = dict(json.loads(file.read()))
        with open(data_weather, 'r')as file:
            cities = dict(json.loads(file.read()))
            city = choice(list(cities.keys()))
            temp = cities[city]
        context = {"sections": sections}
        context.update(super().update_context())
        return render(request, 'main_page.html', context)


class NewList(ListView, ContextAbstract):
    model = New
    template_name = 'section_list.html'

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return likes_control_ajax(self, request)
        else:
            super().get(request, *args, **kwargs)
    # else:
    #    return super().get(request)

    def check_sort_field(self):
        if 'sort_field' in self.request.POST.keys():
            return Section.objects.get(title=self.kwargs['section_title']).new_set.all().order_by(
                self.request.POST['sort_field'])
        else:
            return Section.objects.get(title=self.kwargs['section_title']).new_set.all()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['logged'] = self.request.user.is_authenticated
        context['news_list'] = self.check_sort_field()
        context['sections'] = Section.objects.all()
        context['current_section'] = Section.objects.get(title=self.kwargs['section_title'])
        context.update(super().update_context())

        return context


class NewDetail(DetailView, ContextAbstract):
    model = New
    context_object_name = 'news'
    template_name = 'new_detail.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sections'] = Section.objects.all()
        context['current_new'] = New.objects.get(id=self.kwargs['pk'])
        text_len = len(New.objects.get(id=self.kwargs['pk']).text)
        if New.objects.get(id=self.kwargs['pk']).picture:
            textend_part1 = int(text_len / 3)
            textend_part2 = textend_part1 * 2
            context['text_part1'] = New.objects.get(id=self.kwargs['pk']).text[:textend_part1] + '-'
            context['text_part2'] = New.objects.get(id=self.kwargs['pk']).text[textend_part1:textend_part2] + '-'
            context['text_part3'] = New.objects.get(id=self.kwargs['pk']).text[textend_part2:]

        context.update(super().update_context())

        return context


class NewCreate(CreateView, ContextAbstract):
    form_class = NewForm
    model = New
    template_name = 'create_new.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sections'] = Section.objects.all()
        context['current_section'] = Section.objects.get(title=self.kwargs['title'])

        context.update(super().update_context())

        return context
