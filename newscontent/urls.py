from django.urls import path
from .views import NewListView, NewDetailView, NewCreateView, MainPageView, rate_update
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('update/', rate_update, name='rate_update'),
    path('<str:title>/<int:pk>/', NewDetailView.as_view(), name='new_detail'),
    path('<str:title>/create_news/', NewCreateView.as_view(), name='create_new'),
    path('sections/<str:section_title>/', NewListView.as_view(), name='section_list'),
    path('', MainPageView.as_view(), name='main_page'),


] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL,
                                                                                           document_root=settings.MEDIA_ROOT)
