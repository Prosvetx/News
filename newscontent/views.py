# from django.views.generic.list import ListView
# from django.views.generic.detail import DetailView
import json
from django.http import HttpResponse, JsonResponse

from .tasks import update_rates

from newscontent.logic.url_logic import NewList, NewDetail, NewCreate, MainView


class MainPageView(MainView):
    """Main index page"""


class NewListView(NewList):
    """List of news in Sections host/section"""


class NewDetailView(NewDetail):
    """Detail news from NewListView host/section/id"""


class NewCreateView(NewCreate):
    """Create news post host/section/create_news"""


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
    # else:
    #    return HttpResponse('privet')
