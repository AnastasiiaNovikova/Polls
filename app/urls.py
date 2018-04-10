from django.conf.urls import url
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    # url(r'^$', views.index, name='index'),
    url(r'^polls_list/$', views.polls_list, name='polls_list'),
    url(r'^polls/(?P<poll_id>[0-9]+)/$', views.poll, name='poll'),
    url(r'^choose/$', views.choose, name='choose'),
    url(r'^login/$', auth_views.login, name='login'),
    url(r'^logout/$', auth_views.logout, name='logout'),
]

