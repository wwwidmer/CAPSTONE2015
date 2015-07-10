"""Capstone URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.core.urlresolvers import reverse_lazy
from django.views.generic import RedirectView
from menu import views

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'menu.views.index'),
    url(r'^ajax/food/','menu.views.ajax_get_food_by_id'),
    url(r'^ajax/menu/','menu.views.ajax_get_menu_by_id'),
    url(r'^ajax/menu/food/','menu.views.ajax_get_food_by_menu_id'),
    url(r'^ajax/review/','menu.views.ajax_get_review_by_food'),
    url(r'^menus/food/(?P<f_id>\d+)', 'menu.views.render_food'),
    url(r'^menus/food/type/(?P<t_id>\d+)', 'menu.views.render_browse_type_food'),
    url(r'^menus/gid/(?P<g_id>[^/]+)/(?P<name>\w+)', 'menu.views.render_menu_by_gid'),
    url(r'^menus/gid/(?P<g_id>[^/]+)', 'menu.views.render_menu_by_gid'),
    url(r'^menus/(?P<m_id>[^/]+)', 'menu.views.render_menu'),
    url(r'^menus/type/(?P<t_id>\d+)', 'menu.views.render_browse_type_food'), #(?P<m_id>\d+)
    url(r'^menus/type/', 'menu.views.render_browse_type_index'),
    url(r'^menus', 'menu.views.render_browse_top_menu'),
    url(r'^search/results', 'menu.views.render_search'),
    url(r'^search/', 'menu.views.render_search_index'),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
]
