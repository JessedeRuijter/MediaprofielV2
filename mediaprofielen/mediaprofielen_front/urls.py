from django.conf.urls import patterns, url
from django.contrib.auth.views import login, logout
from mediaprofielen_front import views

urlpatterns = patterns('',
    url(r'^$', views.homeView, name='home'),
    url(r'^login/$', login, name='login'),
    url(r'^logout/$', logout, {'next_page':'/login'}, name='logout'),
)