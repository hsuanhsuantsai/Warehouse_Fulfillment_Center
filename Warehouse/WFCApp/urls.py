from django.conf.urls import url, include

from .views import *
from django.contrib.auth import views as auth_views

# app_name = 'WCFApp'
urlpatterns = [
     url(r'^$', home, name='home'),
     url(r'^QuickStart/$', QuickStart, name='QuickStart'),
     url(r'^documentation/$', documentation, name='documentation'),
     url(r'^accounts/login/$', auth_views.login, name='login'),
     url(r'^accounts/logout/$', logout, name='logout'),
     url(r'^accounts/register/$', register, name='register'),
     url(r'^accounts/delete/$', deleteAccount, name='deleteAccount'),
     url(r'^oauth/', include('social_django.urls', namespace='social')),
     url(r'^settings/$', settings, name='settings'),
     url(r'^settings/password/$', password, name='password'),
     url(r'^(?P<api>[a-zA-Z0-9-]+)/inventory/$', inventory, name='inventory'),
     url(r'^(?P<api>[a-zA-Z0-9-]+)/inventory/(?P<sku>[a-zA-Z0-9-]+)/$', item, name='item'),
     url(r'^(?P<api>[a-zA-Z0-9-]+)/orders/$', orders, name='orders'),
]