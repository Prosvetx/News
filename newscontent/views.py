# from django.views.generic.list import ListView
# from django.views.generic.detail import DetailView

# from .models import Section, New
from newscontent.logic.url_logic import NewList, NewDetail, NewCreate, MainView


class MainPageView(MainView):
    """Main index page"""



class NewListView(NewList):
    """List of news in Sections host/section"""


class NewDetailView(NewDetail):
    """Detail news from NewListView host/section/id"""


class NewCreateView(NewCreate):
    """Create news post host/section/create_news"""
