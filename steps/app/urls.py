from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from . import views
from app.views import *

app_name = 'app'
urlpatterns = [
    url(r'^login/$', auth_views.login, name='login', kwargs={'redirect_authenticated_user': True}),
    url(r'^logout/$', auth_views.logout,{'next_page': '/'}, name='logout'),
    url(r'^$', views.index, name='index'),
    url(r'^dashboard/$', views.dashboard, name='dashboard'),
    #url(r'^incubator/$', views.incubator, name='incubator'),
    url(r'^leaderboard/$', views.leaderboard, name='leaderboard'),
    url(r'^comparator/$', views.comparator, name='comparator'),
    #url(r'^startup/$', views.startup, name='startup'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate, name='activate'),
    url(r'^request/incubator/$', views.incubator_request, name='incubator_request'),
    url(r'^request/startup/$', views.startup_request, name='startup_request'),
    url(r'^update/incubator/$', views.incubator_update, name='incubator_update'),
    url(r'^profile/(?P<username>\w+)/$', profile, name='profile'),
    url(r'^update/startup/$', views.startup_update, name='startup_update'),
    url(r'^update/user/$', views.user_update, name='user_update'),
    url(r'^update_contact/$', views.contact_add, name = 'update_contact'),
    url(r'^update_achievement/$', views.achievement_add, name = 'update_achievement'),
    url(r'^update_social/$', views.social_add, name = 'update_social'),
    url(r'^add/incubator/$', views.incubator_member_add, name='incubator_member_add'),
    url(r'^approve/incubator/(?P<id>[0-9]+)/$', views.approve_incubator, name='approve_incubator'),
    url(r'^reject/incubator/(?P<id>[0-9]+)/$', views.reject_incubator, name='reject_incubator'),
    url(r'^approve/incubator/(?P<id>[0-9]+)/$', views.approve_startup, name='approve_incubator'),
    url(r'^reject/incubator/(?P<id>[0-9]+)/$', views.reject_startup, name='reject_incubator'),
    url(r'^add/startup/$', views.startup_member_add, name='startup_member_add'),
    url(r'^all/incubators/$', views.all_incubators, name='all_incubators'),
    url(r'^all/startups/$', views.all_startups, name='all_startups'),

]
