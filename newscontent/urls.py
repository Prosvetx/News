from django.urls import path, include, reverse_lazy
from .views import (NewListView, NewDetailView, NewCreateView, MainPageView, rate_update,
                    likes_update, search_page, dashboard, loggout, LogginView, PasswordRestView, PasswordRestDoneView,
                    PasswordRestConfirmView, PasswordRestCompleteView, register, all_rates)
from django.conf import settings
from django.conf.urls.static import static

# from django.contrib.auth import views as auth_views

urlpatterns = [

                  #path('', dashboard, name='dashboard'),
                  path('allrates/', all_rates, name='all_rates'),
                  path('update/', rate_update, name='rate_update'),
                  path('news/<str:title>/<int:pk>/', NewDetailView.as_view(), name='new_detail'),
                  path('news/<str:title>/create_news/', NewCreateView.as_view(), name='create_new'),
                  path('news/<str:section_title>/', NewListView.as_view(), name='news_list'),
                  path('news/', MainPageView.as_view(), name='main_page'),
                  path('likes_update/', likes_update, name='likes_update'),
                  path('search/', search_page, name='search_page'),
                  path('login/', LogginView.as_view(), name='login'),
                  path('logout/', loggout, name='logout'),
                  path('password_reset/', PasswordRestView.as_view(), name='password_reset'),
                  path('password_reset/done/', PasswordRestDoneView.as_view(), name='password_reset_done'),
                  path('reset/<uidb64>/<token>/', PasswordRestConfirmView.as_view(),
                       name='password_reset_confirm'),
                  path('reset/done/', PasswordRestCompleteView.as_view(), name='password_reset_complete'),
                  path('register/', register, name='register'),

              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL,
                                                                                           document_root=settings.MEDIA_ROOT)
