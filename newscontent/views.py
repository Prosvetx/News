import json
from django.http import HttpResponse, JsonResponse
from .logic.ajax_requests.likes import likes_control
from django.shortcuts import render, redirect
from .tasks import update_rates
from .forms import SearchForm, UserRegistrationForm
from .models import New, Rate
from .logic.url_logic import (ContextAbstract, PasswordResView,
                              NewList, NewDetail, NewCreate, MainView, LogView, PasswordResDoneView,
                              PasswordResConfirmView, PasswordResCompleteView)
from django.contrib.postgres.search import SearchVector
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout


# from newscontent.logic.url_logic import


class MainPageView(MainView):
    """Main index page"""


class NewListView(NewList):
    """List of news in Sections host/section"""


class NewDetailView(NewDetail):
    """Detail news from NewListView host/section/id"""


class NewCreateView(NewCreate):
    """Create news post host/section/create_news"""


class LogginView(LogView):
    """Login view, с основным котекстом"""


class PasswordRestView(PasswordResView):
    """Password reset view, через почту"""


class PasswordRestDoneView(PasswordResDoneView):
    """Password reset done, страница отправки письма"""


class PasswordRestConfirmView(PasswordResConfirmView):
    """Password reset confirm, из ссылки внутри письма"""


class PasswordRestCompleteView(PasswordResCompleteView):
    """Password reset complete, страница успешного завершения смены пароля"""


def rate_update(request):
    if request.method == 'POST':
        data = {}
        functions_dict = {'update': update_rates.delay}
        post_data = dict(json.loads(request.body.decode()))
        func = 'func'
        if func in post_data and post_data[func] in functions_dict:
            functions_dict[post_data[func]]()
        else:
            print('nothing')
        return JsonResponse(data, status=200)


def likes_update(request):
    if request.user.is_authenticated:
        return likes_control(request)


def search_page(request):
    form = SearchForm()
    print(request.GET)
    context = {"form": form}

    if 'look_for' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            look_for = form.cleaned_data['look_for']
            print(look_for)
            answer = New.objects.annotate(search=SearchVector('title', 'text')).filter(search=look_for)
            cnt = answer.count()
            if answer:
                context.update({"answer": answer, "cnt": cnt, "look_for": look_for})
            elif not answer:
                context["nope"] = f'Sorry no result :( \
                    for "{look_for}"'
    context.update(ContextAbstract.abstract_context(request))
    context['ntimes'] = 'time'

    return render(request, 'search.html', context)


@login_required
def dashboard(request):
    return render(request, 'account/dashboard.html', {'section': 'dashboard'})


def loggout(request):
    logout(request)
    return redirect(ContextAbstract.main_url + "/news/")


def register(request):
    context = {}
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        context.update(ContextAbstract.abstract_context(request))
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            context.update({'new_user': new_user})
            return render(request, 'registration/register_done.html', context)
        else:
            context.update({"user_form": user_form})
            return render(request, 'registration/register.html', context)
    else:
        user_form = UserRegistrationForm()
        context = {'user_form': user_form}
        context.update(ContextAbstract.abstract_context(request))
        return render(request, 'registration/register.html', context)


def all_rates(request):
    allrates = Rate.objects.all()
    context = {"allrates": allrates}
    context.update(ContextAbstract.abstract_context(request))
    return render(request, 'all_rates.html', context)
